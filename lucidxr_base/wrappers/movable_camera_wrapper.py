import numpy as np
from dm_control.mujoco import MovableCamera


from lucidxr_base.wrappers.multiview_image_wrapper import MultiViewImageWrapper


class MovableCameraWrapper(MultiViewImageWrapper):
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
        if not self.custom_camera:
            return super().render(mode, **kwargs)
        else:
            if "overlays" not in kwargs:
                kwargs["overlays"] = ()
            if "scene_callback" not in kwargs:
                kwargs["scene_callback"] = None
            if "segmentation" not in kwargs:
                kwargs["segmentation"] = False
            if "scene_option" not in kwargs:
                kwargs["scene_option"] = None
            if "render_flag_overrides" not in kwargs:
                kwargs["render_flag_overrides"] = None
            if "depth" not in kwargs:
                if mode == "depth":
                    kwargs["depth"] = True
                else:
                    kwargs["depth"] = False

            camera = MovableCamera(self.unwrapped.env.physics,
                                   height=kwargs["height"],
                                   width=kwargs["width"],
                                   scene_callback = kwargs["scene_callback"])
            camera.set_pose(**self.camera_pose)
            image = camera.render(
                overlays=kwargs["overlays"],
                depth = kwargs["depth"],
                segmentation=kwargs["segmentation"],
                scene_option=kwargs["scene_option"],
                render_flag_overrides=kwargs["render_flag_overrides"],
            )
            camera._scene.free()
            return image

