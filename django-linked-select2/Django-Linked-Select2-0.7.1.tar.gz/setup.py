#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import os

from setuptools import find_packages, setup


def read(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name="Django-Linked-Select2",
    version=__import__("linked_select2").__version__,
    description="Django-Select2 extended with dependant widgets",
    long_description=read("README.md"),
    author="Miron Olszewski",
    author_email="mionolski@gmail.com",
    license="LICENSE.txt",
    url="https://bitbucket.org/merixstudio/django-linked-select2",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django-Select2>=5.8.6',
    ],
)
