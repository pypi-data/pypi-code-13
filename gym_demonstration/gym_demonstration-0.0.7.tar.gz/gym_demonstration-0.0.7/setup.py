import os
import sys

from setuptools import setup

setup(name='gym_demonstration',
      version='0.0.7',
      install_requires=['gym[atari]>=0.2.6',
                        'ujson',
                        'gym-vnc>=0.0.13'],
)
