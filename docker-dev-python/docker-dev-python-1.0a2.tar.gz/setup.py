##############################################################################
#
# Copyright (c) 2016, 2degrees Limited.
# All Rights Reserved.
#
# This file is part of django-pastedeploy-settings
# <https://github.com/2degrees/django-pastedeploy-settings>, which is subject
# to the provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################
from os import path

from setuptools import setup

_HERE = path.abspath(path.dirname(__file__))
_VERSION = open(path.join(_HERE, 'VERSION.txt')).readline().rstrip()
_README = open(path.join(_HERE, 'README.md')).read().strip()

setup(
    name='docker-dev-python',
    version=_VERSION,
    description='Python plugin for development tools for Docker',
    long_description=_README,
    url='https://github.com/2degrees/docker-dev-python',
    author='2degrees',
    author_email='2degrees-floss@googlegroups.com',
    classifiers=[],
    keywords='',
    license='',
    py_modules=['docker_dev_python'],
    install_requires=[
        'docker-dev >= 1.0a2',
    ],
    entry_points={
        'docker_dev.pre_build_hooks': [
            'python = docker_dev_python:build_python_distributions',
        ],
    },
)
