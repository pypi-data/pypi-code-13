# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='physicist',
    version='0.0.1',
    description='Computational physics package',
    long_description=readme,
    author='Jay Woo',
    author_email='jay.woo456456@gmail.com',
    url='https://github.com/jay-woo/Computational-Physics',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
