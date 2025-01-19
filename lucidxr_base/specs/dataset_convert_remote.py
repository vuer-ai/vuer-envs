from lucidxr_base.train.convert_lucidxr_dataset_hd5_remote import main

if __name__ == '__main__':

    main(
        dataset_directory="/lucidxr/lucidxr/datasets/lucidxr/poc/demos/pnp/data/Pancake/2025/01/18/15.54.46/",
        camera_names=["main"],
        vision_key="render_depth",
    )