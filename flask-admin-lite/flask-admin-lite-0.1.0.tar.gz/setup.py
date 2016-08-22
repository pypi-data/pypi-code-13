#!/usr/bin/env python
#coding: utf-8

from setuptools import setup

setup(
    name = "flask-admin-lite",
    author = "wong2",
    author_email = "wonderfuly@gmail.com",
    version = "0.1.0",
    license = "MIT",
    url = "https://github.com/wong2/flask-admin-lite",
    description = "Build lightweight admin panel for your models",
    packages = ['flask_admin_lite'],
    install_requires = ['flask-wtf', 'flask-paginate']
)
