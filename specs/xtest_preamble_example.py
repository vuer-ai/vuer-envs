from vuer_envs.utility import minimize
from vuer_envs.schemas import Mjcf
from vuer_envs.schemas.robot_xmls import Panda


def test_robot_example():
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

    expected_result = """
    
    """

    # todo: add do minified for both
    assert xml._minimized == minimize(expected_result)
