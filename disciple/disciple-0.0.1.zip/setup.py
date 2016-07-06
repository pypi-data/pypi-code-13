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

from setuptools import setup, find_packages

__version__ = '0.0.1'
__author__ = 'Faith Carlson <xuwei0455@github.com>'
__author_email__ = 'xuwei0455@gmail.com'


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
    author_email=__author_email__,
    url='https://github.com/xuwei0455/disciple',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,    
    license='Apache 2.0',
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ),
)
