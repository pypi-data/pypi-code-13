#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2016-07-14 14:55:30
# Filename      : setup.py
# Description   : 

from setuptools import setup

setup(
        name = 'vacuum',
        version = '0.0.2',
        author = 'duoshoubang',
        packages = [
            'vacuum',
            'vacuum.third_party',
            'vacuum.third_party.submail',
            ],
        install_requires = ['cattle'],
        description = 'JJ Bob',
        scripts = ['bin/vacuum'],
        )

