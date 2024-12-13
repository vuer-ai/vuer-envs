from vuer_envs.schemas import Mjcf, MobilePanda


def test_robot_example():
    robot = MobilePanda(
        name="LR_hip_roll",
        pos="0 0 0",
        climit="0 0",
        damping="0",
    )
    robot_2 = MobilePanda(
        name="LR_hip_roll_2",
        pos="0 0 0",
        climit="0 0",
        damping="0",
    )

    xml = Mjcf(robot, robot_2, name="base")

    expected_result = """
    
    """

    assert xml._minimized == expected_result
