#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from jschema import __version__

setup(
    name="jschema",
    version=__version__,
    description="json schema tookit",
    license="MIT",
    author="Stepan Perlov",
    author_email="stepanperlov@gmail.com",
    install_requires=["PyYAML", "jinja2"],
    packages=["jschema", "jschema.make", "jschema.node"],
    package_data={"jschema.make": ["templates/*.j2"]},
    url="https://github.com/stepan-perlov/jschema",
    platforms=["linux"]
)
