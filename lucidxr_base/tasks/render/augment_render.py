import os
from pathlib import Path

import numpy as np
from params_proto import Flag, ParamsProto, Proto
from ml_logger import ML_Logger
import torch
from lucidxr_base import make


class RenderCfg(ParamsProto):
    env_name: str = Proto("lcs:Go1-flat_vision-v1")

    demo_prefix: str = Proto("lcs:Go1-flat_vision-v1")

    render_mode: str = Proto("rgb")

    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    camera_lookat = [0,0,0] # point to look at
    camera_distance = Proto(2) # distance from point
    camera_azimuth = Proto(0) # degrees in x-y plane (from x-axis)
    camera_elevation = Proto(90) # degrees up

    custom_camera = Proto(False)


def render(args: RenderCfg):

    loader = ML_Logger(args.demo_prefix)
    print(loader.get_dash_url())
    df = loader.read_metrics()["metrics.pkl"]
    mocap = df[["ts", "mpos", "mquat"]].dropna()


    env = make(args.env_name, device=args.device, random=0)

    if args.custom_camera:
        env.setCameraPose(args.camera_lookat, args.camera_distance, args.camera_azimuth, args.camera_elevation)

    env.reset()

    frames = []
    for index, row in mocap.iterrows():
        mpos = row.mpos
        mquat = row.mquat
        action = np.hstack([mpos, mquat])[None,...]
        _, _, _, info = env.step(action)
        frames.append(info[f"render_{args.render_mode}"])
        image = frames[-1]
        if image.shape[-1] == 1:
            image = np.repeat(image, 3, axis=-1)
        loader.save_image(image, key=f"render_{args.render_mode}/frame_{index:05d}.png")

    loader.save_video(frames, f"render_{args.render_mode}.mp4")

