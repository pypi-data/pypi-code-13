#!/usr/bin/env python3
import os
from setuptools import setup

setup(
    name='snapstore-publish',
    version='1.0',
    author='Evan Dandrea',
    author_email='ev@ubuntu.com',
    description='Publish a snap to a snapstore',
    license='MIT',
    keywords='snapcraft snap',
    url='https://github.com/evandandrea/snapstore-publish',
    scripts=['snapstore-publish', 'macaroon-create'],
    install_requires=[
        'pymacaroons',
        'requests',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
        ],
)
