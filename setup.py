# read the contents of your README file
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    lines = f.readlines()

# remove images from README
lines = [x for x in lines if ".png" not in x]
long_description = "".join(lines)

setup(
    name="vuer_envs",
    packages=[package for package in find_packages() if package.startswith("vuer_envs")],
    install_requires=[
        "robosuite==1.5.0",
        "mujoco==3.2.6",
    ],
    eager_resources=["*"],
    include_package_data=True,
    python_requires=">=3",
    description="vuer-envs",
    author="Qinxi Yu",
    url="",
    author_email="quincyouxiang@gmail.com",
    version="0.1.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
)