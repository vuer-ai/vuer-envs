# Collecting Demo Data

First install the codebase --- you should be able to see the `collect-demo` commandline program after installation.
**note:** you might want to install dependencies.

```shell
pip install -e .
```

To see the full set of command options, do
```shell
collect-demo --help
```
1. **To visualize mujoco examples, do**
```shell
collect-demo --wd <path-to-save-data> --scene-name adhesion/active_adhesion --port 8012
```

```shell
collect-demo --wd "/Users/ge/Library/CloudStorage/GoogleDrive-ge.ike.yang@gmail.com/My Drive/lucidxr-assets/third_party/mujoco_models" --scene-name adhesion/active_adhesion --port 8012
```


