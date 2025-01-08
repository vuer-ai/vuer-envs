from asyncio import sleep
from glob import glob
from os.path import join
from pathlib import Path
from typing import List

from ml_logger import ML_Logger
from params_proto import ParamsProto, Flag
from termcolor import colored
from vuer.events import ClientEvent
from vuer.schemas import CoordsMarker, Group, Html, span, CatmullRomLine, Line

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

    demo_prefix: str = None

    wd: str = "."
    vuer_port = 8013

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

    vuer = Vuer(static_root=args.wd, port=args.vuer_port)

    loader = ML_Logger(prefix=args.demo_prefix)
    # logger.configure(prefix=args.demo_prefix)

    df = loader.read_metrics()["metrics.pkl"]

    mocap = df[["ts", "mpos", "mquat"]].dropna()
    mocap_traj = df["mpos"].dropna()
    camera_matrix = df[["ts", "camera_matrix"]].dropna()

    @vuer.add_handler("ON_MUJOCO_FRAME")
    async def on_mujoco_frame(event: ClientEvent, proxy: VuerSession):
        # pprint(event.value)
        pass

    with WorkDir(args.wd):
        asset_paths = [join(args.asset_prefix, Path(args.scene_name).parent, asset) for asset in args.assets]
        print(asset_paths[0])

        @vuer.spawn(start=True)
        async def main(proxy: VuerSession):
            frame_stack = camera_matrix.to_dict(orient="records")
            print(f"frame_stake contains {len(frame_stack)} frames.")
            for i, frame in [*enumerate(frame_stack)][::10]:
                ts = frame["ts"]
                mat = frame["camera_matrix"]
                proxy.upsert @ Group(
                    CoordsMarker(key=f"coord.ts-{ts}", scale=0.1),
                    Html(span(f"#{i}", style={"width": 100})),
                    key=f"ts-{ts}",
                    matrix=[*mat],
                )
                await sleep(0.016)

            # # todo: add a ContribLoader to load the MuJoCo plugin.
            # proxy.upsert @ MuJoCo(key="default-sim", src=args.src, assets=asset_paths)
            print([*mocap_traj.values])
            proxy.upsert @ Line(
                key="traj",
                points=[[x, z, -y] for x, y, z in mocap_traj.values],
            )

            while True:
                for frame in mocap.to_dict(orient="records"):
                    ts = frame["ts"]
                    mpos = frame["mpos"]
                    mquat = frame["mquat"]
                    print("mpos", mpos, end="\r", flush=True)

                    proxy.upsert @ MuJoCo(
                        key="default-sim",
                        src=args.src,
                        assets=asset_paths,
                        mpos=[*mpos],
                        mquat=[*mquat],
                    )

                    await sleep(0.016)


if __name__ == "__main__":
    Params.demo_prefix = "/geyang/scratch/2025/01-08/043537"
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
