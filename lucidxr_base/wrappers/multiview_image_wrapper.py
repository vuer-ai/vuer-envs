import numpy as np

from gym_dmc.gym.core import Wrapper


class MultiViewImageWrapper(Wrapper):
    """
    Renders normalized linear depth. This wrapper does NOT apply inversion as in RenderDepthWrapper.
    Output is normalized wrt the specified near and far.
    """

    def __init__(
            self,
            env,
            **_,
    ):
        super().__init__(env)

        self.env = env
        self.custom_camera = False
        self.camera_pose = {"lookat": [0, 0, 0], "distance": 1.0, "azimuth": 0.0, "elevation": -30.0}

    def setCameraPose(self, lookat, distance, azimuth, elevation):
        self.camera_pose = {"lookat": lookat, "distance": distance, "azimuth": azimuth, "elevation": elevation}
        self.custom_camera = True

    def render(self, mode="human", **kwargs):
        if 'camera_id' in kwargs:
            if isinstance(kwargs['camera_id'], list):
                frames = {}
                for camera_id in kwargs['camera_id']:
                    kwargs['camera_id'] = camera_id
                    image = super().render(mode, **kwargs)
                    if len(image.shape) == 2:
                        image = np.expand_dims(image, axis=0)
                    frames[camera_id] = image
                return frames
            else:
                image = super().render(mode, **kwargs)
                if len(image.shape) == 2:
                    image = np.expand_dims(image, axis=0)
                return {kwargs["camera_id"]: image}
