from os import path

from setuptools import setup, find_packages

with open(path.join(path.abspath(path.dirname(__file__)), 'VERSION'), encoding='utf-8') as f:
    version = f.read()

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='vuer-envs',
      packages=find_packages(),
      install_requires=[
          "killport",
          "msgpack",
          "params-proto",
          "numpy",
          "websockets",
          "aiohttp-cors",
          "pillow",
      ],
      description=long_description.split('\n')[0],
      long_description=long_description,
      author='Quincy Yu<quincyouxiang@gmail.com>,Ge Yang<ge.ike.yang@gmail.com>',
      url='https://github.com/vuer-ai/vuer-envs',
      author_email='ge.ike.yang@gmail.com',
      package_data={'vuer-envs': ['vuer_envs', 'vuer_envs/*.*']},
      version=version)
