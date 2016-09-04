#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

from setuptools import setup

setup(
    name = "catechin",
    version = "0.0.1",
    packages = ['catechin'],
    scripts = ['bin/catechin'],
    pakcage_data = {'catechin': ['data/package.xsl']},
)
