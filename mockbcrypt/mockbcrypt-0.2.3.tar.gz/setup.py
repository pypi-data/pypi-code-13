#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='mockbcrypt',
    version='0.2.3',
    description='A bcrypt mock plugin for nosetests',
    long_description=open('README.rst').read(),
    author=', '.join([
        'Bone Yao',
    ]),
    url='https://github.com/boneyao/mockbcrypt',
    packages=['mockbcrypt', ],
    install_requires=[
        'nose',
        'mock'
    ],
    license='MIT',
    entry_points={
        'nose.plugins.0.10': [
            'mockbcrypt = mockbcrypt.plugin:MockBcryptPlugin',
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing',
        'Environment :: Console',
    ],
)
