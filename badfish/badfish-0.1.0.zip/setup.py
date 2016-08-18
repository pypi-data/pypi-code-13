#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

def calculate_version():
    initpy = open('badfish/_version.py').read().split('\n')
    version = list(filter(lambda x: '__version__' in x, initpy))[0].split('\'')[1]
    return version

package_version = calculate_version()

setup(
    name='badfish',
    version=package_version,
    author='Harsh Nisar and Deshana Desai',
    author_email='nisar.harsh@gmail.com',
    packages=find_packages(),
    url='https://github.com/harshnisar/badfish',
    license='License :: OSI Approved :: MIT License',
    description=('Badfish - A missing data analysis and wrangling library in Python'),
    long_description='''
A Python library built over pandas to help wrangle and analyse missing data conveniently.
=============
If you have any questions or comments about badfish, please feel free to contact me via:
E-mail: nisar.harsh@gmail.com or desai.deshna@gmail.com

This project is hosted at https://github.com/harshnisar/badfish
''',
    zip_safe=True,
    install_requires=['pandas', 'seaborn', 'pymining'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ],
    keywords=['data cleaning', 'missing', 'machine learning', 'data analysis', 'imputation', 'data wrangling'],
)