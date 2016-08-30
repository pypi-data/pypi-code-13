#!/usr/bin/env python

from distutils.core import setup

setup(name='ezPyChart',
      version='0.2',
      description='A command line tool to create pie charts from simple tabular data',
      author='Cristian Esquivias',
      url='https://github.com/cesquivias/ezpychart',
      license='GPLv3+',
      scripts=['bin/ezpychart'],
      install_requires=['matplotlib>=1.5'])
