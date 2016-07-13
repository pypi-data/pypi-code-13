#!/usr/bin/env python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages

def find_requirements():
    with open('requirements.txt', 'r') as f:
        return [l.strip() for l in f.readlines()if l.strip() != '']

setup(
    name='peche',
    version='0.1.0',
    author='Mihir Singh (@citruspi)',
    author_email='hello@mihirsingh.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=find_requirements()
)
