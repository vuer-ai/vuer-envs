from vuer_envs.schemas import Link


def test_link():
    link = Link(name="link, pos='0 0 0', climit='0 0', damping='0'")
    link.asset = '<mesh name="panda_link0_vis_0" file="obj_meshes/link0_vis/link0_vis_0.obj"/>'
    link.content = """
        <body name="panda_left_link2" pos="0 0 0" quat="0.707107 -0.707107 0 0">
            <inertial pos="0 0 -0.1" mass="3" diaginertia="0.3 0.3 0.3" />
            <joint name="panda_left_link2_joint2" pos="0 0 0" axis="0 0 1" limited="true" range="-1.7628 1.7628" damping="0.1" />
            <geom mesh="panda_link2_vis" material="panda_Part__Feature024" type="mesh" contype="0" conaffinity="0" group="1" />
        </body>
        """
    expected = """\
<body name="link, pos='0 0 0', climit='0 0', damping='0'">\
<body name="panda_left_link2" pos="0 0 0" quat="0.707107 -0.707107 0 0">\
<inertial pos="0 0 -0.1" mass="3" diaginertia="0.3 0.3 0.3"/>\
<joint name="panda_left_link2_joint2" pos="0 0 0" axis="0 0 1" limited="true" range="-1.7628 1.7628" damping="0.1"/>\
<geom mesh="panda_link2_vis" material="panda_Part__Feature024" type="mesh" contype="0" conaffinity="0" group="1"/>\
</body>\
</body>\
"""

    assert link._minimized == expected


if __name__ == "__main__":
    test_link()
