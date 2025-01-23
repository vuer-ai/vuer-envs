from lucidxr_base.traj_samplers import unroll

if __name__ == "__main__":
    unroll.main(
        checkpoint = "/geyang/scratch/2025/01-18/132031/checkpoints/policy_epoch_1100_seed_100.pt",
        env_name="ur5_basic-pnp-depth-v1",
        vision_key="render_depth",
        render=True,
        num_steps=500,
    )
    # unroll.main(
    #     env_name="ur5_basic-v1",
    #     vision_key="render_rgb",
    #     render=True,
    #     num_steps=100,
    # )



