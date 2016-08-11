#!/usr/bin/env python
from setuptools import setup

setup(
    name='python-varnishadm',
    version='0.2.2',
    long_description=open('README.rst').read(),
    description='Simple Python interface for the Varnish management port',
    author='Justin Quick',
    author_email='justquick@gmail.com',
    url='http://github.com/ByteInternet/python-varnishadm',
    scripts=['bin/varnish_manager'],
    py_modules=['varnishadm'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
)
