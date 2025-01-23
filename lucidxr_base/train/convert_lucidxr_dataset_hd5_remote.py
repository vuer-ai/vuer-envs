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
import jaynes


class ConvertCfg(ParamsProto):
    dataset_directory: str = "/lucidxr/lucidxr/datasets/lucidxr/poc/demos/ability/2021/10/25/14.45.48/"
    verbose = False
    camera_names = ["main"]
    vision_key: str = Proto("render_depth")

    def __post_init__(self, _deps=None):
        for k, v in self.__dict__.items():
            if isinstance(v, str):
                value = v.format(**self.__dict__)
                setattr(self, k, value)


def process_episode(episode, **_deps):
    args = ConvertCfg(**_deps)
    loader = ML_Logger(prefix=args.dataset_directory)
    dataset_path = os.path.join(f"{episode}.hdf5")
    data_dict = {
        "/observations/prop": [],
        "/action": [],
    }
    for cam_name in ConvertCfg.camera_names:
        data_dict[f"/observations/images/{cam_name}"] = []

    traj_file = os.path.join(f"{episode}", "metrics.pkl")
    try:
        df = loader.read_metrics(path=traj_file)[traj_file]
        mocap_traj = df[["ts", "mpos", "mquat"]].dropna()
        for i, index in enumerate(mocap_traj.index):
            if i == len(mocap_traj["ts"]) - 1:
                break
            if index == 3:
                continue
            prop_obs = np.hstack([mocap_traj["mpos"][index], mocap_traj["mquat"][index]])
            action = np.hstack \
                ([mocap_traj["mpos"][mocap_traj.index[i + 1]], mocap_traj["mquat"][mocap_traj.index[i + 1]]])
            data_dict["/observations/prop"].append(prop_obs)
            data_dict["/action"].append(action)
            img_path = os.path.join(f"{episode}", args.vision_key, f"frame_{index:05d}.png")
            try:
                img = Image.open(loader.load_file(img_path))
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
        with h5py.File(f"tmp{os.path.dirname(episode)}.hdf5", "w", rdcc_nbytes=1024 ** 2 * 2) as root:
            root.attrs["sim"] = True
            obs = root.create_group("observations")
            image = obs.create_group("images")
            for name, array in data_dict.items():
                array = np.stack(array)
                root.create_dataset(name, data=array)
        loader.upload_file(f"tmp{os.path.dirname(episode)}.hdf5", dataset_path)
        # just check that it opens
        # args.loader.download_file(dataset_path ,to=f"tmp{episode_idx}.hdf5")
        # sleep(60)
        with h5py.File(f"tmp{os.path.dirname(episode)}.hdf5", "r") as root:
            pass
        os.remove(f"tmp{os.path.dirname(episode)}.hdf5")
        return True
    except Exception as e:
        print(f"Error saving HDF5 for episode {os.path.dirname(episode)}: {e}")
        return None




def main(**_deps):
    args = ConvertCfg(**_deps)

    loader = ML_Logger(prefix=args.dataset_directory)
    episode_dirs = loader.glob("*/")
    num_episodes = len(episode_dirs)

    jaynes.config()
    for episode in episode_dirs:
        jaynes.add(process_episode, episode=episode, **_deps)

    jaynes.execute()
    jaynes.listen()


"""
Take a directory (contains episode folders)
Each episode contains a trajectory.pkl file & a folder of rendered images
"""
