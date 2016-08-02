#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup


with open('requirements.txt') as f:
    dependencies = f.read().splitlines()

setup(
        name='oplevelse',
        version='0.0.1',
        description='The Oplevelse CLI',
        url='https://github.com/oplevelse/oplevelse-cli',
        author='Platon Korzh',
        author_email='platon@korzh.io',
        install_requires=dependencies,
        packages=['cli'],
        entry_points={
            'console_scripts': [
                'oplevelse=cli.main:main'
            ]
        }
)
