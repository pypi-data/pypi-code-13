#!/usr/bin/env python
from distutils.core import setup

VERSION = open('VERSION').read()

setup(
    name='useless-py',
    version=VERSION,
    packages=['useless'],
    url='https://github.com/Code-ReaQtor/useless-py',
    download_url='https://github.com/Code-ReaQtor/useless-py/tarball/{}'.format(VERSION),
    license='MIT',
    author='Ronie Martinez',
    author_email='ronmarti18@gmail.com',
    description='Useful python utilities with less effort.',
    long_description=open('README').read(),
    keywords=[],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'Topic :: Utilities'],
    requires=['gevent']
)
