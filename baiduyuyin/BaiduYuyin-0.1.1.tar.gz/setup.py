#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

import sys
if sys.version_info < (2, 6):
    print("THIS MODULE REQUIRES PYTHON 2.6 OR LATER. YOU ARE CURRENTLY USING PYTHON " + sys.version)
    sys.exit(1)

import BaiduYuyin

setup(
    name="BaiduYuyin",
    version=BaiduYuyin.__version__,
    packages=["BaiduYuyin"],
    include_package_data=True,

    # PyPI metadata
    author=BaiduYuyin.__author__,
    author_email="wuwenjie718@gmail.com",
    description=BaiduYuyin.__doc__,
    long_description=open("README.rst").read(),
    license=BaiduYuyin.__license__,
    keywords="baidu voice service",
    url="https://github.com/wwj718/PyBaiduYuyin",
)
