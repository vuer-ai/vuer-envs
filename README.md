# Vuer Envs

## Setting Up

If you want to develop then install it in editable mode.
```shell
conda create -n vuer-envs python=3.11
pip install -e '.[dev]'
```

## Old Notes, Need @quincy to clean up.


1. first download the assets using rclone
    ```shell
    rclone sync -P remote:lucidxr-assets ./assets
    ```
2. install the module. 
    ```shell
    export VUER_ENVS_ASSETS_PATH=$HOME/datasets/vuer-envs/assets/
    pip install 'vuer-envs[assets]'
    ```
   
    If you want to develop then install it in editable mode.
    ```shell
    pip install -e '.[all]'
    ```
   
## Usage

- `room-demo` is a simple demo of the room environment.
    ```shell
    room-demo --room 10
    ```
  (for Quincy: this script should save the xml locally, that you can drag and drop into MuJoCo.app to visualize. We can make it spin up a `vuer` server in the future but let's keep it simple for now.)
   
## 