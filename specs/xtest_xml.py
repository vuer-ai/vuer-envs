from vuer_envs.schemas import Xml, Link, Mjcf


def test_root_element():
    xml = Xml(tag="mujoco", name="base", children=[])
    assert xml.tag == "mujoco"
    assert xml._attributes == {"name": "base"}
    assert xml._children == []

    assert xml.attributes == 'name="base"'
    assert xml._minimized == '<mujoco name="base"/>'


def test_attribute_string():
    xml = Xml(
        name="base",
        position="0 0 0",
        orientation="0 0 0 1",
    )
    assert xml._minimized == '<mujoco name="base" position="0 0 0" orientation="0 0 0 1"/>'


def test_xml_template():
    link = Link(
        name="LR_hip_roll",
        pos="0 0 0",
        climit="0 0",
        damping="0",
    )
    xml = Mjcf(name="base", children=[link])

    assert (
        xml._minimized
        == '<mujoco name="base"><worldbody><link name="LR_hip_roll" pos="0 0 0" climit="0 0" damping="0"/></worldbody></mujoco>'
    )
