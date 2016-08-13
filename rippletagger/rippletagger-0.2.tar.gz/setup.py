# -*- coding: utf-8 -*-
from setuptools import setup

VERSION = '0.2'

setup(
    name='rippletagger',
    packages=["rippletagger"],
    include_package_data=True,
    version=VERSION,
    description='RippleTagger identifies part-of-speech tags (NOUN, VERB...).',
    author=u'Emil Stenström',
    author_email='em@kth.se',
    url='https://github.com/EmilStenstrom/rippletagger/',
    download_url='https://github.com/EmilStenstrom/rippletagger/archive/%s.zip' % VERSION,
    install_requires=[],
    tests_require=["nose>=1.3.7", "flake8>=3.0.4"],
    test_suite="nose.collector",
    keywords=['pos-tagging', 'pos-tagger', 'multi-langauge', 'nlp', 'rippletagger'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
    ],
)
