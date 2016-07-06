# -*- coding: utf-8 -*-

# Copyright 2016 Faith Carlson <xuwei0455@github.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, eithrer express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = '0.0.0'
__author__ = 'Faith Carlson <xuwei0455@github.com>'

requirements = [
    'gevent',
    'pyzmq',
    'kazoo>=1.0',
]


setup(
    name='disciple',
    version=__version__,
    description='A multi-access distributed message pattern with ZMQ (pyzmq) and ZooKeeper (kazoo).',
    author=__author__,
    url='https://github.com/xuwei0455/disciple',
    packages=['disciple'],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,    
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ),
)
