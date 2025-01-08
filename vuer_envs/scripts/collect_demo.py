from asyncio import sleep

from params_proto import ParamsProto

from vuer_envs.scripts.util.working_directory_context_manager import WorkDir


class Params(ParamsProto, cli_parse=False):
    """Script for collecting virtual reality demos.

    - install collect_demo.py as a cli
    - write params-proto for setting the work dir etc
    - load an example scene (UR5)
    - ask Yajjy to make a scene with a UR5 and a table
    - add ml-logger prefix/dir structure.
    - document in the docs / Notion page.
    """

    wd: str = "."

    scene_name: str = "scene"
    scene_file: str = "{scene_name}.mjcf.xml"
    assets: str = None

    def __post_init__(self):
        self.scene_file.format(**vars(self))


def main():
    args = Params()

    from vuer import Vuer, VuerSession
    from vuer.schemas import MuJoCo

    vuer = Vuer()

    with WorkDir(args.wd):

        @vuer.spawn(start=True)
        async def main(proxy: VuerSession):
            proxy.add @ MuJoCo(
                key="default-sim",
                src=args.scene_file,
                assets=[],
            )
            while True:
                await sleep(10)


if __name__ == "__main__":
    Params.wd = "/Users/ge/Library/CloudStorage/GoogleDrive-ge.ike.yang@gmail.com/My Drive/lucidxr-assets/third_party/mujoco_models"
    main()

# - [x] install collect_demo.py as a cli
# - [ ] write paramsproto for setting the work dir etc
# - [ ] load an example scene (UR5)
# - [ ] ask Yajjy to make a scene with a UR5 and a table
# - [ ] add ml-logger prefix/dir structure.
# - [ ] document in the docs / Notion page.
