#!/usr/bin/env python

from setuptools import setup, find_packages
from pip.req import parse_requirements
from distutils.util import convert_path
import codecs
import sys

# Load version information
main_ns = {}
ver_path = convert_path('gici_settings/__init__.py')
with codecs.open(ver_path, 'rb', 'utf8') as ver_file:
    exec (ver_file.read(), main_ns)

# install_requires = ['twisted==16.2.0', 'treq==15.1.0']

if sys.version_info < (2, 7):
    # python 2.6 isn't supported
    raise RuntimeError('This version requires Python 2.7+')

setup(
    name='gici_settings',
    version=main_ns['__version__'],
    author='Amit Yogev',
    author_email="amit.yogev90gmail.com",
    description='gici settings',
    license='Apache License Version 2.0',
    platforms=['Any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
    ],
    url="http://gici.co.il",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    zip_safe=False,
    include_package_data=True,
    test_suite='tests'
)
