#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='sunwatcher',
      version='0.2',
      description='Binding to SolarLog HTTP API',
      url='https://bitbucket.org/Lavode/sunwatcher',
      author='Michael Senn',
      author_email='michael@morrolan.ch',
      license='Apache License 2.0',
      packages=find_packages(),
      zip_safe=True,
      install_requires = [
          'requests',
      ],
      scripts = [
      ],
      
)
