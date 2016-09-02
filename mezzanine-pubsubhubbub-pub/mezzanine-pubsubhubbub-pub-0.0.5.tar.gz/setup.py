# -*- coding: utf-8 -*-
"""
   Copyright 2016 Kem

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from setuptools import setup, find_packages

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import mezzanine_pubsubhubbub_pub

setup(
    name='mezzanine-pubsubhubbub-pub',
    version=mezzanine_pubsubhubbub_pub.VERSION,
    url=mezzanine_pubsubhubbub_pub.SITE,
    author=mezzanine_pubsubhubbub_pub.AUTHOR,
    author_email=mezzanine_pubsubhubbub_pub.EMAIL,
    license=mezzanine_pubsubhubbub_pub.LICENSE,
    description='publisher of pubsubhubbub (PuSH) in Mezzanine.',
    long_description=open('README.md').read(),
    keywords='django, mezzanine, pubsubhubbub',
    packages=find_packages(),
    install_requires=('setuptools',
                      'mock',
                      'Mezzanine',
                      'requests',),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent", ],
    zip_safe=False,
    include_package_data=True,
)
