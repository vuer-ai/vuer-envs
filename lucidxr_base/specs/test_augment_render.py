from lucidxr_base.tasks.render.augment_render import RenderCfg, render

if __name__ == "__main__":
    args = RenderCfg()

    args.demo_prefix = "/lucidxr/lucidxr/datasets/lucidxr/datasets/2025/01/16/episode_0002/"
    args.env_name = "ur5_basic-depth-v1"
    args.render_mode = "depth"

    render(args)
