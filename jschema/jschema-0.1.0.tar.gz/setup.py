#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from jschema import __version__

setup(
    name="jschema",
    version=__version__,
    description="json schema tookit",
    license='MIT',
    author="Stepan Perlov",
    author_email="stepanperlov@gmail.com",
    install_requires=["PyYAML", "jinja2"],
    packages=["jschema"],
    package_data={'jschema': ['templates/*.j2']},
    platforms=["linux"]
)
