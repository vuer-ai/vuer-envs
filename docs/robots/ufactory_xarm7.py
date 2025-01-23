from cmx import doc

doc @ """
# Xarm7 and Ufactory Gripper

Here is a simple scene with the xarm7 and the ufactory gripper.
"""

with doc:
    from vuer_envs.schemas.robot_xmls.default_scene import DefaultStage
    from vuer_envs.schemas.robot_xmls.xarm7 import Xarm7
    from vuer_envs.schemas.robot_xmls.ufactory_gripper import UfactoryGripper
    from vuer_envs.utils.file import Save

with doc:

    def build_xarm():
        """here we create a scene with a single panda arm (no gripper)."""

        xarm = Xarm7(name="test_xarm7", pos="0 0 0", quat="0 0 0 1", assets="ufactory_xarm7")
        # panda._xml | Save("panda.mjcf.xml")

        scene = DefaultStage(model="xarm7", children=xarm)
        scene._xml | Save("ufactory_xarm7.mjcf.xml")


with doc:

    def build_xarm_gripper():
        """here we create a scene with a single panda arm and a gripper."""

        gripper = UfactoryGripper(asets="ufactory_xarm7")
        xarm = Xarm7(name="test_xarm7", pos="0 0 0", quat="0 0 0 1", children=gripper, assets="ufactory_xarm7")
        # panda._xml | Save("panda.mjcf.xml")

        scene = DefaultStage(model="xarm7 gripper", children=xarm)
        scene._xml | Save("ufactory_xarm7_gripper.mjcf.xml")


if __name__ == "__main__":
    build_xarm()
    build_xarm_gripper()
