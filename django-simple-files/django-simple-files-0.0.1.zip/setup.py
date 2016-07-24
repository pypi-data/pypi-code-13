# -*- coding: UTF-8 -*-

from os.path import dirname, join

from setuptools import setup, find_packages

with open(join(dirname(__file__), 'VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

APP_NAME = 'django-simple-files'

setup(
    name=APP_NAME,
    version=version,
    description=APP_NAME,
    author="lvjiyong",
    author_email='lvjiyong',
    url="https://github.com/lvjiyong/%s" % APP_NAME,
    license="Apache2.0",
    long_description=open('README.md').read(),
    maintainer='lvjiyong',
    platforms=["any"],
    maintainer_email='lvjiyong@gmail.com',
    include_package_data=True,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[

    ],
)
