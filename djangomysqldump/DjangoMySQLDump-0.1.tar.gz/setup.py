#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='DjangoMySQLDump',
    version='0.1',
    author='Geert Dekkers',
    author_email='geert@djangowebstudio.nl',
    packages=find_packages(),
    scripts=[],
    url='http://pypi.python.org/pypi/DjangoMySQLDump/',
    license='LICENSE.txt',
    description='Simple dump tool to automate dumps, for example during automated deploys',
    long_description=open('README').read(),
    install_requires=[
        "Django",
    ],
    keywords = "django mysql dump"
)