from asyncio import sleep
from glob import glob
from os.path import join
from pathlib import Path
from pprint import pprint
from typing import List

from params_proto import ParamsProto, Flag
from termcolor import colored
from vuer.events import ClientEvent

from vuer_envs.scripts.util.working_directory_context_manager import WorkDir


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

    wd: str = "."
    vuer_port = 8012

    scene_name: str = "scene"
    scene_file: str = "{scene_name}.mjcf.xml"
    assets: List[str] = None
    asset_prefix: str = "http://localhost:{vuer_port}/static"

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

        with WorkDir(Path(self.src_path).parent):
            self.assets = glob("**/*.*", recursive=True)

        if self.verbose:
            print(*self.assets, sep="\n")


def main():
    args = Params()

    from vuer import Vuer, VuerSession
    from vuer.schemas import MuJoCo
    from ml_logger import logger

    logger.job_started()
    print(logger.get_dash_url())

    vuer = Vuer(static_root=args.wd, port=args.vuer_port)

    @vuer.add_handler("CAMERA_MOVE")
    async def on_mujoco_frame(event: ClientEvent, proxy: VuerSession):
        camera = event.value['camera']

        logger.log(
            ts=event.ts,
            camera_matrix=camera['matrix'],
            flush=True,
            silent=True,
        )

    @vuer.add_handler("ON_MUJOCO_FRAME")
    async def on_mujoco_frame(event: ClientEvent, proxy: VuerSession):
        frame = event.value["keyFrame"]

        logger.log(
            ts=event.ts,
            **frame,
            flush=True,
            silent=True,
        )

    with WorkDir(args.wd):
        asset_paths = [join(args.asset_prefix, Path(args.scene_name).parent, asset) for asset in args.assets]
        print(asset_paths[0])

        @vuer.spawn(start=True)
        async def main(proxy: VuerSession):
            # todo: add a ContribLoader to load the MuJoCo plugin.
            proxy.upsert @ MuJoCo(key="default-sim", src=args.src, assets=asset_paths)
            while True:
                await sleep(10)

    logger.job_completed()


if __name__ == "__main__":
    Params.wd = "/Users/ge/Library/CloudStorage/GoogleDrive-ge.ike.yang@gmail.com/My Drive/lucidxr-assets/development/robots"
    Params.scene_name = "universal_robots_ur5e/scene"

    args = Params()

    main()

# - [x] install collect_demo.py as a cli
# - [ ] write paramsproto for setting the work dir etc
# - [ ] load an example scene (UR5)
# - [ ] ask Yajjy to make a scene with a UR5 and a table
# - [ ] add ml-logger prefix/dir structure.
# - [ ] document in the docs / Notion page.
