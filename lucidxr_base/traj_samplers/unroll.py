import random
from collections import defaultdict, deque
from importlib import import_module

import dm_control
import numpy as np
import torch
from matplotlib import colormaps
from params_proto import Flag, ParamsProto, Proto
from tqdm import trange

import lucidxr_base


class Unroll(ParamsProto, prefix="unroll"):
    env_name: str = Proto("ur5_basic-depth-v1")
    checkpoint: str = Proto(None, help="Path to the model checkpoint.")

    offline_mode: bool = Flag("Run the model in offline mode, with downloaded checkpoint.")
    vision_key = Proto(None, help="default does not pass in image observation")

    model_entrypoint = "ACT.policy:get_default_act_policy"

    num_steps = 800
    seed = 100

    vision_delay = 0
    action_delay = 1

    render = Flag("flag for rendering videos")

    log_metrics = Proto(True, help="save the episodic metrics to a results table.")

    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    camera_kwargs: dict = Proto(
        {
            "distance": 1.5,
            "lookat": [0.0, 0.0, 0.0],
            "elevation": -45,
            "azimuth": 90,
        }
    )


def main(_deps=None, **deps):
    from ml_logger import logger
    from lucidxr_base import RUN


    Unroll._update(_deps, **deps)

    try:  # RUN.prefix is a template, will raise error.
        RUN._update(_deps)
        logger.configure(RUN.prefix)
    except KeyError:
        pass

    logger.job_started(Unroll=vars(Unroll))
    print(logger.get_dash_url())

    logger.upload_file(__file__)

    if Unroll.render:
        logger.log_text(
            """
            keys:
            - Unroll.env_name
            - Unroll.delay
            - Unroll.seed
            charts:
            - type: video
              glob: splat_rgb.mp4
            - type: video
              glob: renders.mp4
            - type: video
              glob: ego_renders.mp4
            - type: video
              glob: heightmaps.mp4
            - type: video
              glob: height_samples.mp4
            """,
            ".charts.yml",
            True,
            True,
        )

    # set seeds
    np.random.seed(Unroll.seed)
    torch.manual_seed(Unroll.seed)
    random.seed(Unroll.seed)

    env = lucidxr_base.make(Unroll.env_name, device=Unroll.device, random=Unroll.seed)
    env.setCameraPose(**Unroll.camera_kwargs)

    print(env)

    module_path = Unroll.model_entrypoint
    module_name, entrypoint = module_path.split(":")
    module = import_module(module_name)
    model_entrypoint = getattr(module, entrypoint)

    actor = model_entrypoint()
    if Unroll.checkpoint is not None:
        state_dict = logger.torch_load(Unroll.checkpoint, map_location=Unroll.device)
        actor.load_state_dict(state_dict)

    actor.to(Unroll.device)
    actor.eval()

    cmap = colormaps.get_cmap("Spectral")

    render_frames = defaultdict(lambda: [])
    visual_buffer = None  # deque([None] * 5, maxlen=5)

    initial_obs = env.reset()
    print(initial_obs)
    initial_action = initial_obs['observations']
    print(initial_action)
    action_buffer = deque([initial_action] * 5, maxlen=5)

    latent = None

    step = 0

    for _ in trange(Unroll.num_steps):
        try:
            action = action_buffer[-1 - Unroll.action_delay]
            obs, reward, done, info = env.step(action)
            if done:
                print("Env reset, ending this trial.")
                break
            step += 1
        except dm_control.rl.control.PhysicsError:
            print("Physics Error, ending this trial.")
            break

        image = info.get(Unroll.vision_key, None)

        if visual_buffer is None:
            visual_buffer = deque([image] * 10, maxlen=10)
        else:
            visual_buffer.append(image)

        obs = obs["observations"]
        obs_input = torch.from_numpy(obs).float().to(Unroll.device)

        image = visual_buffer[-1 - Unroll.vision_delay]
        image = image.transpose(2, 0, 1).copy()
        image = torch.from_numpy(image).float().to(Unroll.device)
        if image.shape[0] == 1:
            image = image.repeat(3, 1, 1)
        image = image.unsqueeze(0)
        image = image.unsqueeze(0)

        with torch.no_grad():
            action, *extra = actor(
                image,
                obs_input,
                vision_latent=latent,
            )
            action = action[:1]
            print(action.shape)
            if len(extra) > 0:
                latent = extra[0]

            action = action.cpu().numpy()
            action_buffer.append(action)

        if not Unroll.render:
            continue

        if "heightmap" in info:
            hp = info["heightmap"]
            hp -= hp.min()
            hp /= hp.max() + 0.01
            hp = cmap(hp)
            render_frames["heightmaps"].append(hp)

        if "height_samples" in info:
            hp = info["height_samples"]
            hp -= hp.min()
            hp /= hp.max() + 0.01
            hp = cmap(hp)
            render_frames["height_samples"].append(hp)

        if "segmented_img" in info:
            segmentation_viz = info["segmented_img"]
            render_frames["segmentation"].append(segmentation_viz)

            for i, m in info["masks"].items():
                render_frames[f"mask_{i}_in"].append(m[0])  # in, for group zero
                render_frames[f"mask_{i}_out"].append(m[1])  # in, for group zero

        if "flow" in info:
            render_frames["flow"].append(info["flow"])
            render_frames["flow_mask"].append(info["flow_mask"])

            if "flow_image" in info:
                render_frames["flow_viz"].append(info["flow_image"])

        if "render_rgb" in info:
            render_frames["render_rgb"].append(info["render_rgb"])

        if "render_depth" in info:
            render_frames["render_depth"].append(info["render_depth"])

        if "midas_depth" in info:
            render_frames["midas_depth"].append(info["midas_depth"])

        if "splat_rgb" in info:
            render_frames["splat_rgb"].append(info["splat_rgb"])

        if "splat_depth" in info:
            render_frames["splat_depth"].append(info["splat_depth"])


    for k, frames in render_frames.items():
        if frames[-1].dtype in ["float32", "float64"]:
            frames = np.stack(frames)
            frames /= max(frames.max(), frames.min())

        fps = 50 * len(frames) // step
        print(f"saving video to {k}.mp4 at fps=", fps)
        logger.save_video(frames, f"{k}.mp4", fps=fps)

    # TODO no get_metrics as of now
    # if Unroll.log_metrics:
    #     # log performance
    #     episodic_metrics = env.unwrapped.env.task.get_metrics()
    #     logger.save_pkl(episodic_metrics, "episode_metrics.pkl", append=True)
    #     logger.print(episodic_metrics)


if __name__ == "__main__":
    main(
        env_name="ur5_basic-depth-v1",
        checkpoint="",
        vision_key="render_depth",
        render=True,
        num_steps=500,
    )
