# Vuer Envs

## Setting Up

1. first download the assets using rclone
    ```shell
    rclone sync -P gdrive:assets ./public/assets
    ```
2. install the module. 
    ```shell
    export VUER_ENVS_ASSETS_PATH=$HOME/datasets/vuer-envs/assets/
    pip install 'vuer-envs[assets]'
    ```
   
    If you want to develop then install it in editable mode.
    ```shell
    pip install -e .
    ```
   
## Usage

- `room-demo` is a simple demo of the room environment.
    ```shell
    room-demo --room 10
    ```
  (for Quincy: this script should save the xml locally, that you can drag and drop into MuJoCo.app to visualize. We can make it spin up a `vuer` server in the future but let's keep it simple for now.)
   
## 