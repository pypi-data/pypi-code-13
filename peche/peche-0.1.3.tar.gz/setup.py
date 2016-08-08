#!/usr/bin/env python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages

setup(
    name='peche',
    version='0.1.3',
    author='Mihir Singh (@citruspi)',
    author_email='hello@mihirsingh.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'termcolor==1.1.0'
    ]
)
