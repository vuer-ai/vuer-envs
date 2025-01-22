<h1 class="full-width" style="font-size: 49px">welcome to <code style="font-size: 1.3em; background-clip: text; color: transparent; background-image: linear-gradient(to right, rgb(0,140,220), rgb(226,213,79), rgb(210,0,12));">vuer-envs</code><span style="font-size: 0.3em; margin-left: -0.5em; margin-right:-0.4em;">｣</span></h1>

<link rel="stylesheet" href="_static/title_resize.css">

```shell
pip install 'vuer_envs[all]=={VERSION}'
```

Here is an example that loads a URDF file and displays it in the browser. For a more comprehensive list of examples, please refer to
the [examples](examples/01_trimesh) page.

```python
from vuer import Vuer, VuerSession
from vuer.schemas import DefaultScene, Urdf

app = Vuer()


@app.spawn(start=True)
async def main(session: VuerSession):
    app.set @ DefaultScene(
        Urdf("assets/urdf/robotiq.urdf"),
    )

    while True:
        await session.sleep(0.1)
```

<iframe src="https://vuer.ai/?background=131416,fff&collapseMenu=true&initCamPos=2.8,2.2,2.5&scene=3gAEqGNoaWxkcmVukt4AB6hjaGlsZHJlbpCjdGFnpFVyZGaja2V5rHBlcnNldmVyYW5jZaNzcmPZRGh0dHBzOi8vZG9jcy52dWVyLmFpL2VuL2xhdGVzdC9fc3RhdGljL3BlcnNldmVyYW5jZS9yb3Zlci9tMjAyMC51cmRmq2pvaW50VmFsdWVz3gAAqHJvdGF0aW9uk8s%2F%2BR64YAAAAAAAqHBvc2l0aW9ukwAAy7%2F4AAAAAAAA3gAHqGNoaWxkcmVukKN0YWekVXJkZqNrZXmvbWFycy1oZWxpY29wdGVyo3NyY9lAaHR0cHM6Ly9kb2NzLnZ1ZXIuYWkvZW4vbGF0ZXN0L19zdGF0aWMvcGVyc2V2ZXJhbmNlL21ocy9NSFMudXJkZqtqb2ludFZhbHVlc94AAKhyb3RhdGlvbpPLP%2FkeuGAAAAAAAKhwb3NpdGlvbpMAyz%2FR64UgAAAAyz%2FgAAAAAAAArGh0bWxDaGlsZHJlbpCrcmF3Q2hpbGRyZW6QqmJnQ2hpbGRyZW6Q" width="100%" height="400px" frameborder="0"></iframe>

- take a look at the basic tutorial or the tutorial for robotics:
    - [Vuer Basics](tutorials/basics)
    - [Tutorial for Roboticists](tutorials/robotics)
- or try to take a look at the example gallery [here](examples/01_trimesh)

For a comprehensive list of visualization components, please refer to
the [API documentation on Components | vuer](https://docs.vuer.ai/en/latest/api/vuer.html).

For a comprehensive list of data types, please refer to
the [API documentation on Data Types](https://docs.vuer.ai/en/latest/api/types.html).

<!-- prettier-ignore-start -->

```{eval-rst}
.. toctree::
   :hidden:
   :maxdepth: 1
   :titlesonly:

   Quick Start <quick_start>
   Report Issues <https://github.com/vuer-ai/vuer-envs/issues?q=is:issue+is:closed>
   CHANGE LOG <CHANGE_LOG.md>
   
.. toctree::
   :maxdepth: 3
   :caption: Tutorials
   :hidden:
   
   tutorials/basics.md
   tutorials/robotics.md
   tutorials/camera/README.md
   tutorials/physics.md
   
.. toctree::
   :maxdepth: 3
   :caption: Examples
   :hidden:
   
   Simple Scene <examples/01_panda_army.md>
   Collecting Demos <examples/01_collecting_demo.md>
   
.. toctree::
   :maxdepth: 3
   :caption: Python API
   :hidden:
   
   .schemas.base <api/base.md>
   .schemas.mujoco_schema <api/mujoco_schema.md>
   .schemas.robot_xmls.robot_schema <api/robot_schema.md>
   .schemas.robot_xmls.panda <api/panda.md>
  
```
