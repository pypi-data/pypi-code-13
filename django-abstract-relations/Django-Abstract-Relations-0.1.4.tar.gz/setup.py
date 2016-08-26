#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import os

from setuptools import find_packages, setup


def read(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with codecs.open(file_path, encoding='utf-8') as open_file:
        return open_file.read()


PACKAGE = 'abstract_relations'
NAME = 'Django-Abstract-Relations'
DESCRIPTION = 'Dynamically generated customizable through model for abstract many-to-many relations in Django'
AUTHOR = 'Miron Olszewski'
AUTHOR_EMAIL = 'mionolski@gmail.com'
URL = 'https://github.com/molski/django-abstract-relations'
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read('README.md'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='LICENSE.txt',
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.9',
    ],
    zip_safe=False,
)
