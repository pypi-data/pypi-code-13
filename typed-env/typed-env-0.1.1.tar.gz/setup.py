#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

requirements = []

test_requirements = [
    'twine==1.7.4'
]

setup(
    name='typed-env',
    version='0.1.1',
    description="Fast-fail environment variable library.",
    author="Maxim Kurnikov",
    author_email='maxim.kurnikov@gmail.com',
    url='https://github.com/mkurnikov/typed-env',
    license="MIT",

    install_requires=requirements,
    tests_require=test_requirements,
    packages=find_packages(exclude=['typed_env.tests'])
)
