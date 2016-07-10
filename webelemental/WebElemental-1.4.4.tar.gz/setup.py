#!/usr/bin/env python
#coding:utf-8
# Author:  smeggingsmegger
# Purpose: setup
# Created: 2016-06-23
#
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '%s' not found.\n" % fname

long_description = read('README.md')

if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

setup(
    name='WebElemental',
    version='1.4.4',
    url='http://github.com/IntuitiveWebSolutions/WebElemental',
    license='MIT',
    author='Scott Blevins',
    author_email='scottblevins@gmail.com',
    description='An elemental force for driving web pages using Selenium and Python.',
    long_description= long_description+'\n'+read('CHANGES'),
    platforms='OS Independent',
    packages=['WebElemental'],
    include_package_data=True,
    install_requires=['xvfbwrapper', 'selenium'],
    keywords=['Selenium', 'Testing'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
