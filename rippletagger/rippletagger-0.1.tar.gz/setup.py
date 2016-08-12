# -*- coding: utf-8 -*-
from setuptools import setup

VERSION = '0.1'

setup(
    name='rippletagger',
    packages=["rippletagger"],
    version=VERSION,
    description='RippleTagger identifies part-of-speech tags (NOUN, VERB...).',
    author=u'Emil Stenström',
    author_email='em@kth.se',
    url='https://github.com/EmilStenstrom/rippletagger/',
    download_url='https://github.com/EmilStenstrom/rippletagger/archive/%s.zip' % VERSION,
    install_requires=[],
    keywords=['pos-tagging', 'pos-tagger', 'multi-langauge', 'nlp', 'rippletagger'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
    ],
)
