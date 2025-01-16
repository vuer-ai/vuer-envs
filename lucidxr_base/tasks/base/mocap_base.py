import collections

import numpy as np
from dm_control import mujoco
from dm_control.suite import base
from dm_env import specs


class MocapPhysics(mujoco.Physics):
    """
    Acts a wrapper for mujoco.Physics

    Allows commanding mocap points in the underlying MuJoCo sim
    """
    def set_mocap(self, action):
        """
        Command mocap points to follow the action
        :param action: 6 DOF end-effector pose ([[x, y, z, qw, qx, qy, qz]])
                shape is (num_mocap_points, 7)
        :return: nothing
        """
        mpos = action[:, :3]
        mquat = action[:, 3:]
        # MuJoCo uses unit quaternions
        if (np.linalg.norm(mquat) - 1) > 1e-3:
            mquat = mquat / np.linalg.norm(mquat)
        self.data.mocap_pos[:] = mpos
        self.data.mocap_quat[:] = mquat

    def get_mocap(self):
        """
        Get the current pose of the mocap points
        :return: 6 DOF end-effector pose ([[x, y, z, qw, qx, qy, qz]])
                shape is (num_mocap_points, 7)
        """
        mpos = self.data.mocap_pos
        mquat = self.data.mocap_quat
        return np.hstack([mpos, mquat])


class MocapTask(base.Task):
    """
    Base class for Mocap tasks.

    Change the Action space to End-Effector trajectories by commanding mocap points
    """

    def before_step(self, action, physics: MocapPhysics):
        """
        Command mocap points to follow the action
        Overrides the superclass method, which sets the control input for all of the actuators
        :param action: 6 DOF end-effector pose
        :param physics:
        :return: nothing
        """
        physics.set_mocap(action)

    def get_observation(self, physics):
        """
        Get the observation from the physics
        :param physics:
        :return: TODO
        """
        obs = collections.OrderedDict()
        obs["mocap_pos"] = physics.data.mocap_pos
        obs["mocap_quat"] = physics.data.mocap_quat
        obs["observations"] = np.concatenate([obs["mocap_pos"], obs["mocap_quat"]], axis=-1)
        return obs

    def get_reward(self, physics):
        return 0

    def action_spec(self, physics):
        """
        Returns a `BoundedArraySpec` matching the End-Effector pose
        See dm_control/mujoco/engine.py
        """
        num_actions = 7
        # TODO not quite right for unit quaternion but ok for now
        is_limited = np.array([False, False, False, True, True, True, True])
        control_range = np.array([[-mujoco.mjMAXVAL, mujoco.mjMAXVAL],
                                  [-mujoco.mjMAXVAL, mujoco.mjMAXVAL],
                                  [-mujoco.mjMAXVAL, mujoco.mjMAXVAL],
                                  [-1, 1],
                                  [-1, 1],
                                  [-1, 1],
                                  [-1, 1]])
        minima = np.full(num_actions, fill_value=-mujoco.mjMAXVAL, dtype=float)
        maxima = np.full(num_actions, fill_value=mujoco.mjMAXVAL, dtype=float)
        minima[is_limited], maxima[is_limited] = control_range[is_limited].T

        return specs.BoundedArray(
          shape=(num_actions,), dtype=float, minimum=minima, maximum=maxima)

