import lucidxr_base.utils.convert_lucidxr_dataset_hd5 as convert


if __name__ == "__main__":
    convert.main(
        dataset_directory="/lucidxr/lucidxr/datasets/lucidxr/datasets/2025/01/15/",
        camera_names=["main"],
        vision_key="render_depth",
    )


