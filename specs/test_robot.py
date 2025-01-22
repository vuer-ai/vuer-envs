from vuer_envs import Body
from vuer_envs.schemas import Mjcf
from vuer_envs.schemas.robot_xmls import Panda
from vuer_envs.utils.file import Save
from vuer_envs.utils.minimizer import minimize, minimize_many
from vuer_envs.utils.whitener import whiten


def test_body_preamble():
    robot = Body(
        preamble='<asset><inertial mass="0.1"/></asset>',
    )
    assert robot.preamble == '<asset><inertial mass="0.1"/></asset>'


def test_nested_preamble():
    part_1 = Body(
        preamble='<asset><material name="pinku" mass="10" rgba="1.0 0 0 0.3"/></asset>',
    )
    robot = Body(
        part_1,
        preamble='<asset><material name="black" mass="0.1"/></asset>',
    )
    assert (
        robot.preamble | minimize_many
        == """
        <asset>
            <material name="black" mass="0.1"/>
            <material name="pinku" mass="10" rgba="1.0 0 0 0.3"/>
        </asset>
        """
        | minimize_many
    )


def xtest_two_robots():
    robot = Panda(
        name="LR_hip_roll",
        pos="0 0 0",
        climit="0 0",
        damping="0",
    )
    robot_2 = Panda(
        name="LR_hip_roll_2",
        pos="0 0 0",
        climit="0 0",
        damping="0",
    )

    xml = Mjcf(robot, robot_2, name="base")

    expected_result = """"""

    xml._xml | Save("output_panda_two_robots.xml")

    # todo: add do minified for both
    assert xml._minimized == minimize(expected_result)


def test_body():
    link = Body(name="link, pos='0 0 0', climit='0 0', damping='0'")
    link.preamble_ = '<mesh name="panda_link0_vis_0" file="obj_meshes/link0_vis/link0_vis_0.obj"/>'
    link.children_ = """
        <body name="panda_left_link2" pos="0 0 0" quat="0.707107 -0.707107 0 0">
            <inertial pos="0 0 -0.1" mass="3" diaginertia="0.3 0.3 0.3" />
            <joint name="panda_left_link2_joint2" pos="0 0 0" axis="0 0 1" limited="true" range="-1.7628 1.7628" damping="0.1" />
            <geom mesh="panda_link2_vis" material="panda_Part__Feature024" type="mesh" contype="0" conaffinity="0" group="1" />
        </body>
        """

    expected = (
        """
        <body name="link, pos='0 0 0', climit='0 0', damping='0'">
        <body name="panda_left_link2" pos="0 0 0" quat="0.707107 -0.707107 0 0">
        <inertial pos="0 0 -0.1" mass="3" diaginertia="0.3 0.3 0.3"/>
        <joint name="panda_left_link2_joint2" pos="0 0 0" axis="0 0 1" limited="true" range="-1.7628 1.7628" damping="0.1"/>
        <geom mesh="panda_link2_vis" material="panda_Part__Feature024" type="mesh" contype="0" conaffinity="0" group="1"/>
        </body>
        </body>
        """
        | whiten
    )

    assert link._minimized == expected


if __name__ == "__main__":
    test_body()
