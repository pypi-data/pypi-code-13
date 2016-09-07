#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

from setuptools import setup, find_packages

from unique_uploadto import __version__


with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='django-unique-uploadto',
    version=__version__,
    description='Use a unique filename for django uploads',
    long_description=readme,
    author='Ionata Digital',
    author_email='webmaster@ionata.com.au',
    url='https://github.org/ionata/django-unique-uploadto',
    license='BSD',
    packages=find_packages(),
    install_requires=[
        'django>=1.8.0',
    ],

    package_data={},
    include_package_data=True,

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
    ],
)
