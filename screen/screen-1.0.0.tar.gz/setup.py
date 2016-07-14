# -*- coding: utf-8 -*-

from __future__ import with_statement

from setuptools import Extension, setup


version = '1.0.0'


setup(
    name='screen',
    version=version,
    keywords='',
    description='Screen width and so on',
    long_description=open('README.rst').read(),

    url='https://github.com/Brightcells/screen',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    ext_modules=[Extension('screen.str_util', sources=['source/str_util.c'])],
    packages=['screen'],
    py_modules=[],
    install_requires=[],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
