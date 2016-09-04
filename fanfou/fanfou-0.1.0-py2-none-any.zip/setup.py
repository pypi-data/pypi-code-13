#!/usr/bin/env python

from setuptools import setup
from fanfou import __version__

setup(name='fanfou',
      version=__version__,
      description='OAuth of Fanfou',
      author='Akgnah',
      author_email='akgnah@setq.me',
      url=' http://github.com/akgnah/fanfou-oauth',
      packages=['fanfou'],
      long_description="please see the test.py",
      license="MIT",
      platforms=["any"],
      keywords='fanfou oauth',
     )
