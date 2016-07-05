#!/bin/env python3
# from distutils.core import setup
from setuptools import setup
from wswrapper import __version__
import sys

modulename = 'wswrapper'

def readme():
    with open('README.rst') as f:
        return f.read()

print('Current version: ', __version__)
version = __version__.split('.')


if sys.argv[-1] == 'minor':
    version[2] = str(int(version[2]) + 1)
    del sys.argv[-1]
elif sys.argv[-1] == 'major':
    version[1] = str(int(version[1]) + 1)
    version[2] = '0'
    del sys.argv[-1]
elif sys.argv[-1] == 'huge':
    version[0] = str(int(version[0]) + 1)
    version[1] = '0'
    version[2] = '0'
    del sys.argv[-1]


version = '.'.join(version)
with open(modulename + '/version', 'w') as f:
    f.write(version)


setup(
    name=modulename,
    packages=[modulename],  # this must be the same as the name above
    version=version,
    include_package_data=True,
    license='MIT',
    description='Wrapps a socket.socket object to handle the RFC6455 websocket protocol',
    long_description=readme(),
    author='Christoffer Zakrisson',
    author_email='christoffer_zakrisson@hotmail.com',
    url='https://github.com/Zaeb0s/ws-wrapper',
    keywords=['wrapper', 'websocket', 'socket', 'RFC6455', 'wrap'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Programming Language :: Python :: 3.5',
                 'Operating System :: POSIX :: Linux',
                 'License :: OSI Approved :: MIT License'],
    install_requires=['pycrypto']
)


print('Installed version: ' + version)
