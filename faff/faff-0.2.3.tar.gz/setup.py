#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
import setuptools

root = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(root, "README.rst"), "r") as f:
    long_description = f.read()

setuptools.setup(
    name="faff",
    version="0.2.3",
    url="https://github.com/mojzu/faff",
    license="Public Domain",
    author="mojzu",
    author_email="mail@mojzu.net",
    description="Make build tool substitute written in Python.",
    long_description=long_description,
    packages=setuptools.find_packages(
        exclude=["doc", "examples", "tests"],
    ),
    include_package_data=True,
    install_requires=[
        "colorama>=0.3.7",
        "Jinja2>=2.8",
    ],
    entry_points={
        "console_scripts": [
            "faff = faff.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Build Tools",
    ],
    zip_safe=False,
    # Test suite uses Tox, nose and coverage.
    test_suite="nose.collector",
    tests_require=[
        "coverage>=4.2",
        "nose>=1.3.7",
    ],
)
