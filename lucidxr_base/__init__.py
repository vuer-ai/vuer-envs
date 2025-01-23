import os
from contextlib import contextmanager
from importlib import import_module

from gym_dmc.gym.core import Wrapper

from lucidxr_base.wrappers.lucid_env import LucidEnv
from lucidxr_base.wrappers.movable_camera_wrapper import MovableCameraWrapper


# # register all envs
# from .tasks import chase, gaps, hurdle, parkour, stairs
#
# assert [gaps, hurdle, stairs, parkour, chase]


@contextmanager
def ChDir(dir):
    original_wd = os.getcwd()
    os.chdir(dir)
    print("changed work directory to", dir)
    try:
        yield
    finally:
        os.chdir(original_wd)
        print("now changed work directory back.")


ALL_ENVS = {}


def add_env(env_id, entrypoint, kwargs, strict=True):
    if strict and env_id in ALL_ENVS:
        raise RuntimeError(
            f"environment with id {env_id} has already been "
            f"registered. Set strict=False to overwrite."
        )
    ALL_ENVS[env_id] = {
        "entry_point": entrypoint,
        "kwargs": kwargs,
    }


def make(env_id: str, **kwargs) -> MovableCameraWrapper:
    try:
        module_name, env_name = env_id.split(":")
    except ValueError:
        env_name = env_id
        module_name, *_ = env_id.split("-")
        module_name = module_name.lower()

    # relative to the lucidsim name space.
    import_module("lucidxr_base.tasks." + module_name)

    env_spec = ALL_ENVS.get(env_name)

    if env_spec is None:
        raise ModuleNotFoundError(
            f"Environment {env_id} is not found. You can choose between:\n{ALL_ENVS}."
        )

    entry_point = env_spec["entry_point"]
    _kwargs = env_spec.get("kwargs", {})
    _kwargs.update(kwargs)

    env = entry_point(**_kwargs)

    return env

from ml_logger import logger
from ml_logger.job import RUN, instr

RUN.prefix = "/lucidxr/lucidxr/{file_stem}/{job_name}"

assert logger, "for export"

if __name__ == "__main__":
    fn = instr(lambda: None, __diff=False)
    print(logger.prefix)
    print(logger.get_dash_url())

