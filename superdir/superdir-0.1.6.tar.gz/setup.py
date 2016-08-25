# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup

def read(fname):

    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

    except IOError as E:
        print('Could not open {}'.format(fname))
        print(E)


setup(
    name = "superdir",
    author = 'Alex Ramsdell',
    author_email = 'alexramsdell@gmail.com',
    version = '0.1.6',
    url = 'http://github.com/foundling/superdir',
    license = 'MIT',
    description = 'Turn that text file into a file tree!',
    keywords = 'cli productivity',
    packages = ['superdir'],
    scripts = ['bin/superdir'],
    long_description = read('README.md'),
    install_requires = [
        'click'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
