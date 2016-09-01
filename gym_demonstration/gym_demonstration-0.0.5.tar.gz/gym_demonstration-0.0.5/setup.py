import os
import sys

from setuptools import setup

setup(name='gym_demonstration',
      version='0.0.5',
      install_requires=['gym[atari]>=0.2.3', 'ujson', 'gym-vnc>=0.0.12'],
)
