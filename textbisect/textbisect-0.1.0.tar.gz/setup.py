#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name="textbisect",
    version="0.1.0",
    license="GPL3",
    description="Binary search in a sorted text file",
    author="Antonis Christofides",
    author_email="antonis@antonischristofides.com",
    url="https://github.com/openmeteo/textbisect",
    packages=find_packages(),
    test_suite="tests",
)
