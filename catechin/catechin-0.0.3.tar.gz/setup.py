#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

from setuptools import setup

setup(
    name = "catechin",
    author = "Yuki Furuta",
    author_email = "furushchev@jsk.imi.i.u-tokyo.ac.jp",
    version = "0.0.3",
    packages = ['catechin'],
    entry_points = {'console_scripts': ['catechin=catechin:main']},
    package_data = {'catechin': ['data/package.xsl']},
    url = 'https://github.com/furushchev/catechin',
    install_requires = [
        'cdiff==0.9.8',
        'cmakelists-parsing>=0.3',
        'colorama>=0.2.5',
        'lxml>=3.3.3',
    ]
)
