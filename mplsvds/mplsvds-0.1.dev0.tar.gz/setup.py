#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='mplsvds',
    version='0.1.dev0',
    author='Daniel Margala',
    author_email='daniel@svds.com',
    packages=['mplsvds', 'mplsvds.test'],
    # license='LICENSE.txt',
    description='matplotlib styling for svds',
    long_description=open('README.md').read(),
    install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'pandas',
          'seaborn',
      ],
)
