from cmx import doc

doc @ """
# Xarm7 and Ufactory Gripper

Here is a simple scene with the xarm7 and the ufactory gripper.
"""

with doc:
    from vuer_envs import DefaultStage, Robotiq2F85
    from vuer_envs.utils.file import Save, Prettify

with doc:

    def build_gripper():
        """here we create a scene with a single panda arm (no gripper)."""

        gripper = Robotiq2F85(name="robotiq-2f85", assets="robotiq_2f85")
        # panda._xml | Save("panda.mjcf.xml")

        scene = DefaultStage(model="robotiq-2f85", children=gripper)
        scene._xml | Prettify() | Save("robotiq_2f85.mjcf.xml")




if __name__ == "__main__":
    build_gripper()
