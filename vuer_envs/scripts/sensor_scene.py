import colorsys
from asyncio import sleep
from collections import deque
from datetime import datetime
from glob import glob
from os.path import join
from typing import List
import random

import numpy as np
import serial
import time

from params_proto import ParamsProto, Flag
from termcolor import colored
from vuer.events import ClientEvent
from vuer.schemas import Box, span, Html, group, Line, HandActuator, Hands, Scene, AmbientLight

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

    scene_folder: str = ""
    scene_name: str = "scene"
    scene_file: str = join("{scene_folder}", "{scene_name}.mjcf.xml")

    demo_prefix: str = "lucidxr/lucidxr/datasets/lucidxr/scene_init/{scene_folder}"

    # asset_prefix: str = "http://localhost:{vuer_port}/static"
    asset_prefix: str = "https://adam-2.ngrok.app/static"
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



class ArduinoMotorController():
    def __init__(self, serial_port='/dev/ttyACM0') -> None:
        self.serial_port = serial_port
        self.ser = serial.Serial(self.serial_port, 9600, timeout=2)
        self.adaptive_thresholds = [0, 0, 0, 0, 0, 0]

    def control_motors_with_pwm(self, signal_values, thresholds, signal_maxes):
        pwm_values = []
        for value, threshold, s_max in zip(signal_values, thresholds, signal_maxes):
            pwm_value = max(0, min(255, int((value - threshold) * 255 / (s_max - threshold))))
            pwm_values.append(pwm_value)
            self.ser.write(f"{pwm_value} ".encode())
        print("PWM values sent: ", pwm_values)

    def stop_motors(self):
        for _ in range(20):
            self.ser.write("0 ".encode())
        print('Motors stopped')


def main():
    args = Params()

    from vuer import Vuer, VuerSession
    from vuer.schemas import MuJoCo
    from ml_logger import logger

    vuer = Vuer(static_root=args.wd, port=args.vuer_port)

    box_state = "#23aaff"
    box_other = "#54f963"

    frame = {}

    controller = ArduinoMotorController('/dev/cu.usbmodem11301')

    @vuer.add_handler("ON_MUJOCO_FRAME")
    async def on_mujoco_frame(event: ClientEvent, proxy: VuerSession):
        nonlocal frame

        frame = event.value["keyFrame"]
        # print("Frame:", frame.keys())

    with WorkDir(args.wd):

        @vuer.spawn(start=True)
        async def main(proxy: VuerSession):
            nonlocal frame
            await sleep(5)

            # proxy.set @ Scene(
            #     bgChildren=[
            #         # Fog(color=0x2c3f57, near=1, far=7),
            #         Hands(scale=1.05),
            #         AmbientLight(),
            #     ],
            # )
            # await sleep(0.0005)

            # todo: add a ContribLoader to load the MuJoCo plugin.
            proxy.upsert @ MuJoCo(
                HandActuator(key="pinch-on-squeeze", high=0.01, low=255, ctrlId=-1),
                key="default-sim",
                src=args.src,
                assets=args.asset_paths,
                keyFrame=["sensordata"],
            )



            while True:
                if "sensordata" in frame:
                    finger1, finger2 = frame["sensordata"]
                    controller.control_motors_with_pwm([finger1, finger2, 0.01, 0.01, 0.01], [0, 0, 0, 0, 0], [30, 30, 30, 30, 30])
                await sleep(0.05)


if __name__ == "__main__":
    # Params.wd = "/Users/yajvanravan/Library/CloudStorage/GoogleDrive-yravan@mit.edu/.shortcut-targets-by-id/1UQnuWv4ICaE50w_nPTTNeZ1_YtRsswuX/lucidxr-assets/development/robots"
    # Params.wd = "/Users/abrashid/Library/CloudStorage/GoogleDrive-abrashid@mit.edu/.shortcut-targets-by-id/1UQnuWv4ICaE50w_nPTTNeZ1_YtRsswuX/lucidxr-assets/development/robots"
    Params.wd = "/Users/abrashid/mit/lucid_xr/assets/"

    Params.scene_name = "scene"
    Params.scene_folder = "sensor"

    args = Params()

    main()
