#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='monitoring_agent',
      version='0.1.2',
      description='Agent to collect system metrics for Linux machines',
      author='Aditya Patawari',
      author_email='aditya@adityapatawari.com',
      url='https://github.com/adimania/monitoring_agent',
      license='GPLv3',
      install_requires=['psutil'],
      scripts=['bin/monitoring-agent'],
      packages=find_packages(),
     ) 

