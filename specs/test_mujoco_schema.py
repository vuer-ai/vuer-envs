from vuer_envs.schemas import MjcfNode


def test_mjcf_node():
    mjcf = MjcfNode(
        tag="body",
        attributes=""" name="test_name" """,
        children=[
            "<geom type='box' size='0.1 0.1 0.1' rgba='1 0 0 1'/>",
            "<site name='test_site' pos='0 0 0' size='0.002' rgba='1 0 0 -1'/>",
        ],
        preamble="""<asset> <texture type='2d' name='test_texture' file='rooms/assets/textures/flat/light_gray.png'/> </asset>""",
    )

    assert mjcf._minimized == '<body name="test_name"><geom type="box" size="0.1 0.1 0.1" rgba="1 0 0 1"/><site name="test_site" pos="0 0 0" size="0.002" rgba="1 0 0 -1"/></body>'


if __name__ == "__main__":
    test_mjcf_node()