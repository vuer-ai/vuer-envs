from lucidxr_base.traj_samplers import unroll

if __name__ == "__main__":
    unroll.main(
        checkpoint = "/yajvan/scratch/2025/01-16/160418/checkpoints/policy_best_epoch_7.pt",
        env_name="ur5_basic-depth-v1",
        vision_key="render_depth",
        render=True,
        num_steps=100,
    )
    unroll.main(
        env_name="ur5_basic-v1",
        vision_key="render_rgb",
        render=True,
        num_steps=100,
    )



