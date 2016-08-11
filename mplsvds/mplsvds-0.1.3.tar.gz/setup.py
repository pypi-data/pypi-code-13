#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='mplsvds',
    version='0.1.3',
    author='Daniel Margala',
    author_email='daniel@svds.com',
    packages=['mplsvds', 'mplsvds.test'],
    # license='LICENSE.txt',
    description='matplotlib styling for svds',
    long_description=long_description,
    install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'pandas',
          'seaborn',
      ],
)
