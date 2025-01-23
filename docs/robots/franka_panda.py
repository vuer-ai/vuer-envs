from cmx import doc

doc @ """
# Panda Arm (with Tomika Gripper)

Here is a simple scene with a panda arm and a tomika gripper.
"""

with doc:
    from vuer_envs.schemas.robot_xmls.default_scene import DefaultStage
    from vuer_envs.schemas.robot_xmls.panda import Panda
    from vuer_envs.schemas.robot_xmls.tomika_gripper import TomikaGripper
    from vuer_envs.utils.file import Save

with doc:

    def build_panda():
        """here we create a scene with a single panda arm and a tomika gripper"""

        panda = Panda(name="test_panda", pos="0 0 0", quat="0 0 0 1", assets="franka_panda")
        # panda._xml | Save("panda.mjcf.xml")

        scene = DefaultStage(model="panda-tomika", children=panda)
        scene._xml | Save("franka_panda.mjcf.xml")


build_panda()

with doc:

    def build_panda_tomika():
        """here we create a scene with a single panda arm and a tomika gripper"""

        tomika = TomikaGripper(name="tomika-1")
        # tomika._xml | Save("panda.mjcf.xml")

        panda = Panda(name="test_panda", pos="0 0 0", quat="0 0 0 1", end_effector=tomika)
        # panda._xml | Save("panda.mjcf.xml")

        scene = DefaultStage(model="panda-tomika", children=panda)
        scene._xml | Save("framka_panda_tomika.mjcf.xml")


build_panda_tomika()


doc.flush()
