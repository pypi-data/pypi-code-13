#!/usr/bin/env python

from setuptools import setup

setup(
    name='SkyFish',
    version='0.3.4',
    description='Official Skyfish Inventory Integration SDK for Merchants',
    long_description="Skyfish merchants can use this as the simplest way to integrate and sync their inventory to skyfish merchants",
    author='Fauzan Emmerling',
    author_email='erich@emfeld.com',
    url='https://github.com/coralhq/skyfish-py-sdk',
    license='MIT',
    packages=['skyfish','skyfish.models'],
    install_requires=['requests'],
    zip_safe=False)
