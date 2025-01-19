from asyncio import sleep
from glob import glob
from os.path import join
from typing import List

from ml_logger import ML_Logger
from params_proto import ParamsProto, Flag
from termcolor import colored
from vuer.events import ClientEvent
from vuer.schemas import Line, MuJoCo

from vuer_envs.scripts.util.working_directory_context_manager import WorkDir

import colorsys


def hsv_to_uint8(h, s, v):
    """
    Convert HSV values to a uint8 array representing RGB values.

    Parameters:
    h (float): Hue value, should be in the range [0, 1].
    s (float): Saturation value, should be in the range [0, 1].
    v (float): Value (brightness), should be in the range [0, 1].

    Returns:
    np.ndarray: A uint8 array with RGB values.
    """
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return [r * 255, g * 255, b * 255]


class Params(ParamsProto, cli_parse=False):
    """Script for collecting virtual reality demos.

    - [x] install collect_demo.py as a cli
    - [x] write params-proto for setting the work dir etc
    - [x] load an example scene (UR5)
    - [ ] add logic to glob and find all files in the directory
    - ask Yajjy to make a scene with a UR5 and a table
    - add ml-logger prefix/dir structure.
    - document in the docs / Notion page.
    """

    demo_prefix: str = None

    wd: str = "."
    vuer_port = 8012

    scene_folder: str = ""
    scene_name: str = "scene"
    scene_file: str = join("{scene_folder}", "{scene_name}.mjcf.xml")

    asset_prefix: str = "http://localhost:{vuer_port}/static"
    assets: List[str] = None
    asset_paths: List[str] = None

    src: str = "{asset_prefix}/{scene_file}"
    src_path: str = "{wd}/{scene_file}"

    verbose = Flag(help="Print out the assets that are being loaded.")

    def __post_init__(self):
        for k, v in self.__dict__.items():
            if isinstance(v, str):
                value = v.format(**self.__dict__)
                setattr(self, k, value)

                if self.verbose:
                    print(f"{colored(k, 'cyan')}:\t{colored(value, 'yellow')}")

        with WorkDir(join(self.wd, self.scene_folder)):
            self.assets = glob("**/*.*", recursive=True)
            self.asset_paths = [join(self.asset_prefix, self.scene_folder, asset) for asset in self.assets]

        if self.verbose:
            print("Assets:")
            print(*self.assets, sep="\n")
            print("Asset Paths:")
            print(*self.asset_paths, sep="\n")


def main():
    args = Params()

    from vuer import Vuer, VuerSession

    vuer = Vuer(static_root=args.wd, port=args.vuer_port)

    loader = ML_Logger(prefix=args.demo_prefix)

    print(loader)
    metrics = loader.read_metrics(path="**/metrics.pkl")
    print(metrics.keys())

    @vuer.add_handler("ON_MUJOCO_FRAME")
    async def on_mujoco_frame(event: ClientEvent, proxy: VuerSession):
        # pprint(event.value)
        pass

    with WorkDir(args.wd):

        @vuer.spawn(start=True)
        async def main(proxy: VuerSession):
            proxy.upsert @ MuJoCo(
                key="default-sim",
                src=args.src,
                assets=args.asset_paths,
            )

            # Setup the scene with Fog to simulate MuJoCo's default style.
            for i, (key, df) in enumerate(metrics.items()):
                # mocap = df[["ts", "mpos", "mquat"]].dropna()
                try:
                    mocap_traj = df["mpos"].dropna()
                    # camera_matrix = df[["ts", "camera_matrix"]].dropna()

                    proxy.upsert @ Line(
                        key=f"traj-{key}",
                        points=[[x, z, -y] for x, y, z in mocap_traj.values],
                        color=hsv_to_uint8(i / len(metrics), 1, 1),
                        lineWidth=0.1,
                    )
                except KeyError:
                    print("no stuff")

            while True:
                await sleep(5)


if __name__ == "__main__":
    Params.demo_prefix = "/lucidxr/lucidxr/datasets/lucidxr/poc/demos/pnp/data/universal_robots_ur5e/2025/01/18/23.48.11"
    Params.wd = "/Users/abrashid/mit/lucid_xr/assets/"
    Params.scene_name = "scene"
    Params.scene_folder = "universal_robots_ur5e"

    args = Params()

    main()

# - [x] install collect_demo.py as a cli
# - [ ] write paramsproto for setting the work dir etc
# - [ ] load an example scene (UR5)
# - [ ] ask Yajjy to make a scene with a UR5 and a table
# - [ ] add ml-logger prefix/dir structure.
# - [ ] document in the docs / Notion page.
