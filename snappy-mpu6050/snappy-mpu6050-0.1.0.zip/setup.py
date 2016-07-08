#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='snappy-mpu6050',
    description="Synapse SNAPpy library for Ivensense MPU-6050 6-axis accelerometer/gyro",
    maintainer='Tyler Crumpton',
    maintainer_email='tyler.crumpton@gmail.com',
    url='https://github.com/tylercrumpton/snappy-mpu6050',
    packages=['snappy_mpu6050'],
    setup_requires=['vcversioner'],
    vcversioner={
        'version_module_paths': ['snappy_mpu6050/_version.py'],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
    ],
)
