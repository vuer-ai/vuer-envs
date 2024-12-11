import argparse
import numpy as np
import robosuite as suite
from robosuite.environments.manipulation import manipulation_env

import vuer_envs.environments.base

def main(env_name):
    # create environment instance
    env: manipulation_env = suite.make(
        env_name=env_name, # try with other tasks like "Stack" and "Door"
        robots="Panda",  # try with other robots like "Sawyer" and "Jaco"
        has_renderer=True,
        has_offscreen_renderer=False,
        use_camera_obs=False,
    )

    # reset the environment
    env.reset()

    while True:
        action = np.random.randn(*env.action_spec[0].shape) * 0.1
        obs, reward, done, info = env.step(action)  # take action in the environment
        env.render()  # render on display
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, default="LivingRoomLift")
    args = parser.parse_args()
    main(args.env)