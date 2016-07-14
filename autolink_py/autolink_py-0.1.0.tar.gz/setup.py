#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

from autolink_py import __version__

setup(
    name='autolink_py',
    version=__version__,
    # Your name & email here
    author='Tzeng',
    author_email='tseng0211@gmail.com',
    # If you had autolink_py.tests, you would also include that in this list
    packages=find_packages(),
    # Any executable scripts, typically in 'bin'. E.g 'bin/do-something.py'
    scripts=[],
    # REQUIRED: Your project's URL
    url='https://github.com/joanne-tseng/autolink_py',
    # Put your license here. See LICENSE.txt for more information
    license='',
    # Put a nice one-liner description here
    description='',
    long_description=open('README.md').read() if exists("README.md") else "",
    # Any requirements here, e.g. "Django >= 1.1.1"
    install_requires=[
        
    ],
)
