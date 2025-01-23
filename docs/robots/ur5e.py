from cmx import doc


doc @ """
# Xarm7 and Ufactory Gripper

Here is a simple scene with the xarm7 and the ufactory gripper.
"""

with doc:
    from vuer_envs import UR5e, DefaultStage, Robotiq2F85
    from vuer_envs.utils.file import Save, Prettify

with doc:

    def build_ur5e():
        """here we create a scene with a single uR5e arm (no gripper)."""

        ur5e = UR5e(name="ur5e", assets="ur5e")
        # ur5e._xml | Prettify() | Save("ur5e.mjcf.xml")

        scene = DefaultStage(model="ur5e", children=ur5e)
        scene._xml | Prettify() | Save("ur5e.mjcf.xml")


with doc:

    def build_ur5e_robotiq():
        """here we create a scene with a single uR5e arm and a gripper."""

        gripper = Robotiq2F85(assets="robotiq_2f85")
        ur5e = UR5e(name="ur5e", assets="ur5e", end_effector=gripper)
        # ur5e._xml | Prettify() | Save("ur5e.mjcf.xml")

        scene = DefaultStage(model="ur5e", children=ur5e)
        scene._xml | Prettify() | Save("ur5e_robotiq_2f85.mjcf.xml")


if __name__ == "__main__":
    build_ur5e()
    build_ur5e_robotiq()
