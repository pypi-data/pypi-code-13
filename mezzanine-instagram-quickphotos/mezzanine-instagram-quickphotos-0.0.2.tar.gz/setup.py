#!/usr/bin/env python
from codecs import open

from setuptools import find_packages, setup


with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name='mezzanine-instagram-quickphotos',
    version='0.0.2',
    description='Latest Photos from Instagram for Mezzanine',
    long_description=readme,
    url='https://github.com/kmlebedev/mezzanine-instagram-quickphotos',
    maintainer='Konstantin Lebedev',
    maintainer_email='lebedev.k.m@gmail.com',
    platforms=['any'],
    install_requires=[
        'Mezzanine>=4.1.0',
        'python-instagram>=0.8.0',
    ],
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='BSD',
)
