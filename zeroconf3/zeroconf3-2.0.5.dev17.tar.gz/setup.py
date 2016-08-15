#!/usr/bin/env python

from setuptools import setup
setup(setup_requires=['pbr>=1.8', 'pytest-runner>=2.8', 'setuptools>=21'],
      tests_require=['pytest'], pbr=True)
