#!/usr/bin/env python
# coding=utf8

from setuptools import setup, find_packages

setup(
    name="change-build",
    version="0.0.1",
    keywords=("pip", "deployment", "build", "change"),
    description="change build",
    long_description="build for change system",
    license="MIT Licence",

    url="http://changedeploy.cloud",
    author="maoxuepeng",
    author_email="maoxuepeng@gmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],

    scripts=[],
    entry_points={
        'console_scripts': [
            'bcl = changebuild.Build:main'
        ]
    }
)
