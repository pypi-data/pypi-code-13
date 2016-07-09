#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
import setuptools
import faff.constants

root = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(root, faff.constants.README), "r") as f:
    long_description = f.read()

setuptools.setup(
    name=faff.constants.NAME,
    version=faff.constants.VERSION,
    url=faff.constants.URL,
    license=faff.constants.LICENCE,
    author=faff.constants.AUTHOR,
    author_email=faff.constants.AUTHOR_EMAIL,
    description=faff.constants.DESCRIPTION,
    long_description=long_description,
    packages=[faff.constants.NAME],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "{0} = {0}.main:main".format(faff.constants.NAME),
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
        "coverage==4.1",
        "nose==1.3.7",
    ],
)
