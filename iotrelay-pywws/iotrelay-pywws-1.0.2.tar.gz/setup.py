#!/usr/bin/env python
import os
from setuptools import setup

project_dir = os.path.abspath(os.path.dirname(__file__))

long_descriptions = []
for rst in ('README.rst', 'LICENSE.rst'):
    with open(os.path.join(project_dir, rst), 'r') as f:
        long_descriptions.append(f.read())

setup(name='iotrelay-pywws',
      version='1.0.2',
      description='pywws source module for iotrelay',
      long_description='\n\n'.join(long_descriptions),
      author='Emmanuel Levijarvi',
      author_email='emansl@gmail.com',
      url='https://github.com/eman/iotrelay-pywws',
      install_requires=['iotrelay', 'pywws'],
      license='BSD',
      py_modules=['iotrelay_pywws'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Utilities',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      keywords='weather IoT',
      entry_points={
          'iotrelay': ['source=iotrelay_pywws:Poll']
      })
