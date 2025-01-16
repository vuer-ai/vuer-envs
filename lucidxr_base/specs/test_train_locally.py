from anyio.lowlevel import checkpoint
from params_proto import ParamsProto
from ACT import train
from lucidxr_base.utils import convert_lucidxr_dataset_hd5 as convert


class TrainingCfg(ParamsProto):
    dataset_dir = "/lucidxr/lucidxr/datasets/lucidxr/datasets/2025/01/16/"


def main():
    convert.main(
        dataset_directory=TrainingCfg.dataset_dir,
        camera_names=["main"],
        vision_key="render_depth",
    )

    train.main(
        dataset_prefix = [
            TrainingCfg.dataset_dir[1:]
        ],
        load_checkpoint = None,
        local_load = False,
        num_epochs = 10,
        checkpoint_interval = 1,
    )



if __name__ == "__main__":
    main()






