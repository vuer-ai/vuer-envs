# Getting Started

To get a quick overview of what you can do with `vuer`, check out the following:

- take a look at the basic tutorial or the tutorial for robotics:
  - [Vuer Basics](tutorials/basics)
  - [Tutorial for Roboticists](tutorials/robotics)
- or try to take a look at the example gallery [here](examples/01_trimesh)

Setting up the conda environment:

```python
conda create -n vuer python=3.8
conda activate vuer
```
Install the newest version of `vuer-envs` from PyPI:
```python
pip install -U 'vuer-envs=={VERSION}'
```

Now you should be able to run scripts show in the examples, and look at the 
results on [vuer.ai](https://vuer.ai). To view the scene in VR or AR headsets, you
need to install `ngrok` (see [setting up ngrok](ngrok.io)) to promote the websocket
to `wss`.

```{admonition} Using ngrok to promote to <code>wss://</code>
:class: tip
You need to install `ngrok` to promote the local vuer server
from ws://localhost:8012 to wss://xxxx.ngrok.io, (note the double
w[ss] in the protocol), and pass it as a query parameter that 
looks like this:

      https://vuer.ai?ws=wss://xxxxx.ngrok.io

Note the repeated `ws` and then `wss://` in the query string.
```

```{admonition} Open3D for Apple Sillicon (2024-03)
:class: tip
The newest version of Open3D seems not compatible with Apple Silicon.
If you are using M1, M2 or M3 macs, install the `open3d==0.15.1` or 
other patches of `0.15`. 
```

## Developing VuerEnvs (Optional)

All examples can be run from the document folder in the vuer repository:
[vuer-envs.git/docs](https://github.com/vuer-ai/vuer-envs/tree/main/docs). First
clone the vuer repo for example code,
```shell
cd ~  # assume working in home directory
git clone https://github.com/vuer-ai/vuer-envs.git
```

If you want to develop vuer, you can install it in editable mode plus dependencies
relevant for building the documentations:
```shell
cd vuer-envs
pip install -e '.[all]'
```
To build the documentations, run the following, then go to http://localhost:8888:
```shell
make docs
```


