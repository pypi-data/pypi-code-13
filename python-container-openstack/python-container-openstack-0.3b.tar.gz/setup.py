#!/usr/bin/python
#coding=utf-8

__author__ = 'Danilo Ferri Perogil'

from distutils.core import setup

setup(name='python-container-openstack',
      version='0.3b',
      description='Python Distribution Utilities for Openstack and Containers',
      author='Danilo Ferri Perogil',
      author_email='dperogil@gmail.com',
      license='Creative Commons Attribution-Noncommercial-Share Alike license',
      url='https://github.com/dperogil',
      long_description=open('README').read(),
      packages=['bootstrap', 'containers', 'dockerfile', 'dockermachine', 'key',
                'linux', 'openstack', 'pykubernetes', 'scripts'],
     )
