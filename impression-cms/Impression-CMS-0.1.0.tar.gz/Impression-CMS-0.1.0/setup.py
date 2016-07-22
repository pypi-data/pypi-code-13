#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    name='Impression-CMS',
    version='0.1.0',
    url='https://smeggingsmegger.github.io/impression/',
    author='Scott Blevins',
    author_email='sblevins@gmail.com',
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'flask',
        'Flask-Assets',
        'Flask-Cache',
        'Flask-Login',
        'Flask-Mail',
        'Flask-Migrate',
        'Flask-Permissions',
        'Flask-Script',
        'Flask-SQLAlchemy',
        'Flask-Themes2',
        'Flask-WTF',
        'simplejson',
        'textile',
        'python-creole',
        'Markdown',
        'pillow',
        'python-dateutil',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points='''
        [console_scripts]
        impression=runserver
    '''
)
