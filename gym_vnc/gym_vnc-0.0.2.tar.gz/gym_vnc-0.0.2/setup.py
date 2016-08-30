import os
import sys

from setuptools import setup

setup(name='gym_vnc',
      version='0.0.2',
      install_requires=['gym>=0.2.3', 'docker-py', 'Pillow', 'autobahn', 'twisted', 'ujson'],
      extras_require={
          'atari': 'gym[atari]',
          # Faster vnc driver
          'go': ['go-vncdriver'],
      }
)
