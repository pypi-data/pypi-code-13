#!/usr/bin/env python
import os
from setuptools import setup

project_dir = os.path.abspath(os.path.dirname(__file__))

long_descriptions = []
for rst in ('README.rst', 'LICENSE.rst'):
    with open(os.path.join(project_dir, rst), 'r') as f:
        long_descriptions.append(f.read())

setup(name='iotrelay_nest',
    version='0.1.0',
    description='IoT Relay plugin for the Nest Thermostat',
    long_description='\n\n'.join(long_descriptions),
    author='Emmanuel Levijarvi',
    author_email='emansl@gmail.com',
    install_requires=['iotrelay', 'pynest'],
    url='https://github.com/eman/iotrelay-nest',
    license='BSD',
    py_modules=['iotrelay_nest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='IoT Relay Nest Temerature Humidity',
    entry_points={
        'iotrelay': ['source=iotrelay_nest:Poll']
    }
)
