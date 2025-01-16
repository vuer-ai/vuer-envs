

"""
This script converts the lucidxr dataset to hd5 format that can be read by Episodic Dataset & used for training
"""
import io
import os
import pickle
from time import sleep

import h5py
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from ml_logger import ML_Logger
from params_proto import ParamsProto, Proto
from tqdm.contrib.concurrent import thread_map


class ConvertCfg(ParamsProto):
    dataset_directory: str = "/lucidxr/lucidxr/datasets/lucidxr/poc/demos/ability/2021/10/25/14.45.48/"
    verbose = False
    camera_names = ["main"]
    vision_key: str = Proto("render_depth")
    loader: ML_Logger = None
    
    def __post_init__(self, _deps=None):
        for k, v in self.__dict__.items():
            if isinstance(v, str):
                value = v.format(**self.__dict__)
                setattr(self, k, value)
    
    def get_num_episodes(self):
        if self.loader is None:
            raise ValueError("Loader not set")
        episode_dirs = self.loader.glob( "*/")
        return len(episode_dirs)
        



def main(**kwargs):
    ConvertCfg._update(kwargs)
    args = ConvertCfg()
    loader = ML_Logger(prefix=args.dataset_directory)
    args.loader = loader
    num_episodes = args.get_num_episodes()
    start_ep = 0

    def process_episode(episode_idx: int):
        dataset_path = os.path.join(f"episode_{episode_idx}.hdf5")
        data_dict = {
            "/observations/prop": [],
            "/action": [],
        }
        for cam_name in ConvertCfg.camera_names:
            data_dict[f"/observations/images/{cam_name}"] = []

        traj_file = os.path.join(f"episode_{episode_idx:04d}", "metrics.pkl")
        try:
            df = args.loader.read_metrics(path=traj_file)[traj_file]
            mocap_traj = df[["ts", "mpos", "mquat"]].dropna()
            for i, index in enumerate(mocap_traj.index):
                if i == len(mocap_traj["ts"]) - 1:
                    break
                if index == 3:
                    continue
                prop_obs = np.hstack([mocap_traj["mpos"][index], mocap_traj["mquat"][index]])
                action = np.hstack([mocap_traj["mpos"][mocap_traj.index[i + 1]], mocap_traj["mquat"][mocap_traj.index[i + 1]]])
                data_dict["/observations/prop"].append(prop_obs)
                data_dict["/action"].append(action)
                img_path = os.path.join(f"episode_{episode_idx:04d}", args.vision_key, f"frame_{index:05d}.png")
                try:
                    img = Image.open(args.loader.load_file(img_path))
                    img = np.array(img)
                    if len(img.shape) == 2:
                        img = np.stack([img, img, img], axis=-1)
                    for cam_name in args.camera_names:
                        data_dict[f"/observations/images/{cam_name}"].append(img)
                except Exception as e:
                    print(f"Failed to load {img_path}")
                    return None  # Fail this episode
        except Exception as e:
            print(f"Error processing trajectory {traj_file}: {e}")
            return None

        max_timesteps = len(mocap_traj["ts"])
        try:
            with h5py.File(f"tmp{episode_idx}.hdf5", "w", rdcc_nbytes=1024 ** 2 * 2) as root:
                root.attrs["sim"] = True
                obs = root.create_group("observations")
                image = obs.create_group("images")
                for name, array in data_dict.items():
                    array = np.stack(array)
                    root.create_dataset(name, data=array)
            sleep(10)
            args.loader.upload_file(f"tmp{episode_idx}.hdf5", dataset_path)
            sleep(10)
            args.loader.download_file(dataset_path, to=f"tmp{episode_idx}.hdf5")
            sleep(10)
            # os.remove(f"tmp{episode_idx}.hdf5")
            return True
        except Exception as e:
            print(f"Error saving HDF5 for episode {episode_idx}: {e}")
            return None

    results = thread_map(process_episode, range(0, num_episodes), max_workers=16, desc="Processing Episodes")

    failed_episodes = [i for i, result in enumerate(results, start=start_ep) if not result]
    if failed_episodes:
        print(f"Failed episodes: {failed_episodes}")
    else:
        print("All episodes processed successfully.")




"""
Take a directory (contains episode folders)
Each episode contains a trajectory.pkl file & a folder of rendered images
"""