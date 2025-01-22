from cmx import doc

doc @ """
# A simple Scene

Here is a simple scene with a panda arm and a tomika gripper.
"""

with doc:
    from vuer_envs import Mjcf
    from vuer_envs.schemas.robot_xmls.panda import Panda
    from vuer_envs.schemas.robot_xmls.tomika_gripper import TomikaGripper
    from vuer_envs.utils.file import Save

with doc:

    def build_one():
        """here we create a scene with a single panda arm and a tomika gripper"""

        tomika = TomikaGripper(name="tomika-1")
        # tomika._xml | Save("panda.mjcf.xml")

        panda = Panda(name="test_panda", pos="0 0 0", quat="0 0 0 1", end_effector=tomika)
        # panda._xml | Save("panda.mjcf.xml")

        scene = Mjcf(model="panda-tomika", children=panda)
        scene._xml | Save("panda.mjcf.xml")


doc @ """
### How about two pandas?

"""
with doc:

    def build_two():
        """here we do two."""

        tomika = TomikaGripper(name="gripper")
        tomika_2 = TomikaGripper(name="gripper_2")

        panda = Panda(name="test_panda", pos="-0.5 0 0", quat="0 0 0 1", end_effector=tomika)
        panda_2 = Panda(name="test_panda_2", pos="0.5 0 0", quat="0 0 0 1", end_effector=tomika_2)

        scene = Mjcf(model="panda-tomika", children=(panda, panda_2))
        scene._xml | Save("panda.mjcf.xml")


doc @ """
### Panda Army

"""
with doc:

    def empire_strikes():
        """now many on a grid."""
        all = tuple()
        for i in range(5):
            for j in range(2):
                # print(f"adding panda {i} {j}")
                tomika = TomikaGripper(name=f"gripper_{i}_{j}")
                panda = Panda(name=f"test_panda_{i}_{j}", pos=f"{i * 0.5} {j * 0.5} 0", quat="0 0 0 1", end_effector=tomika)
                all = all + (panda,)

        scene = Mjcf(model="panda-army", children=all)

        print("saving the scene...")
        scene._xml | Save("panda_army.mjcf.xml")

        print("I am finished.")


doc.flush()

# if __name__ == "__main__":
#     # build_two()
#     empire_strikes()
