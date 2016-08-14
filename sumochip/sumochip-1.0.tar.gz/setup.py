#!/usr/bin/env python3
# coding: utf-8
import os
from setuptools import setup

setup(
    name = "sumochip",
    version = "1.0",
    author = u"Lauri Võsandi",
    author_email = "lauri.vosandi@gmail.com",
    description = "SumoCHIP is an extremely low-budget robotics platform based on CHIP single-board computer",
    license = "MIT",
    keywords = "sumorobot robot nextthingco getchip allwinner arm python flask",
    url = "http://github.com/laurivosandi/sumochip",
    packages=[
        "sumochip",
    ],
    long_description=open("README.md").read(),
    install_requires=[
        "flask",
    ],
    include_package_data = True,
    package_data={
        "sumochip": ["sumochip/templates/*"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
)

