# -*- coding: utf-8 -*-
from io import open
import os
from setuptools import setup

dist_dir = os.path.dirname(os.path.abspath(__file__))
readme = os.path.join(dist_dir, 'README.rst')
with open(readme, 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='colorhash',
    version='1.0.0',
    description='Generate a color based on a value',
    long_description=long_description,
    url='https://bitbucket.org/fk/python-color-hash',
    author='Felix Krull',
    author_email='f_krull@gmx.de',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    py_modules=['colorhash'],
    package_dir={'': 'src'},

    test_suite='test',
)
