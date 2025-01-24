import glob
import os
from typing import Literal

from dm_control.rl import control
from ml_logger import ML_Logger
from skimage.data import camera

from lucidxr_base import add_env, INITIAL_POSITION_PREFIXES
from lucidxr_base.tasks.base.mocap_base import MocapTask, MocapPhysics
from lucidxr_base.wrappers.history_wrapper import HistoryWrapper
from lucidxr_base.wrappers.lucid_env import LucidEnv
from lucidxr_base.wrappers.render_depth_wrapper import RenderDepthWrapper
from lucidxr_base.wrappers.render_rgb_wrapper import RenderRGBWrapper

DEFAULT_TIME_LIMIT = 25
PHYSICS_TIMESTEP = 0.005  # in XML
DECIMATION = 4
CONTROL_TIMESTEP = PHYSICS_TIMESTEP * DECIMATION

UR5_SCENE_FILE = './assets/third_party/adam_robots/universal_robots_ur5e/scene.mjcf.xml'
UR5_PNP_SCENE_FILE = './assets/development/scenes/ur5_pickandplace/scene.mjcf.xml'
INIT_DIR = '/lucidxr/lucidxr/datasets/lucidxr/scene_init/universal_robots_ur5e/'


def entrypoint(
    xml_path,
    # note: we will remove the segmentation because it does not affect the
    #   policy. It is just what we allow the unroll script to collect.
    mode: Literal["heightmap", "vision", "depth", "segmentation", "heightmap_splat"],
    time_limit=DEFAULT_TIME_LIMIT,
    random=None,
    device=None,
    domain_rand=False,
    # for vision
    stack_size=1,
    check_contact_termination=False,
    **kwargs,
):
    physics = MocapPhysics.from_xml_path(xml_path)
    task = MocapTask()
    env = control.Environment(
        physics,
        task,
        time_limit=time_limit,
        control_timestep=CONTROL_TIMESTEP,
    )


    env = LucidEnv(env, height=480, width=270, camera_id=-1, skip_start=3)
    if mode == "depth":
        env = RenderDepthWrapper(
            env,
            width=640,
            height=360,
            camera_id=-1 if "camera_id" not in kwargs else kwargs["camera_id"]
        )
    elif mode == "vision":
        env = RenderRGBWrapper(
            env,
            width=480,
            height=270,
            camera_id=-1 if "camera_id" not in kwargs else kwargs["camera_id"]
        )
    if "history" in kwargs:
        env = HistoryWrapper(env, history_len=4)
    return env

add_env(
    env_id="ur5_basic-v1",
    entrypoint=entrypoint,
    kwargs=dict(
        xml_path=UR5_SCENE_FILE,
        mode="vision",
    ),
)
add_env(
    env_id="ur5_basic-depth-v1",
    entrypoint=entrypoint,
    kwargs=dict(
        xml_path=UR5_SCENE_FILE,
        mode="depth",
    ),
)
add_env(
    env_id="ur5_basic-pnp-v1",
    entrypoint=entrypoint,
    kwargs=dict(
        xml_path=UR5_PNP_SCENE_FILE,
        mode="vision",
        camera_id=["table_pov", "overhead"],
    ),
)
add_env(
    env_id="ur5_basic-pnp-depth-v1",
    entrypoint=entrypoint,
    kwargs=dict(
        xml_path=UR5_PNP_SCENE_FILE,
        mode="depth",
        camera_id=["table_pov", "overhead"],
    ),
)
add_env(
    env_id="ur5_basic-pnp-depth-history-v1",
    entrypoint=entrypoint,
    kwargs=dict(
        xml_path=UR5_PNP_SCENE_FILE,
        mode="depth",
        camera_id=["table_pov", "overhead"],
        history=True,
    ),
)
INITIAL_POSITION_PREFIXES["ur5_basic-pnp-v1"] = INIT_DIR
INITIAL_POSITION_PREFIXES["ur5_basic-pnp-depth-v1"] = INIT_DIR
INITIAL_POSITION_PREFIXES["ur5_basic-pnp-depth-history-v1"] = INIT_DIR
"""
[x] make a simple UR5 environment 
[x] render the depth image
[] functionality for inputing the camera pose
"""
