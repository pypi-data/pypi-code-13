#!/usr/bin/env python

from setuptools import setup

bitbucket_url = 'https://gprohorenko@bitbucket.org/gprohorenko/fabext'

setup(
    name='fabext',
    version='0.1',
    description='Extentions for Fabric',
    long_description=open('README.rst', 'r').read(),
    author='blinchik',
    author_email='prohorenko_gena_@mail.ru',
    download_url='https://bitbucket.org/gprohorenko/fabext/downloads/fabext.tar.gz',
    url=bitbucket_url,
    include_package_data=True,
    license='MIT License',
    zip_safe=False,
    packages=['fabext'],
    install_requires=[
        "Fabric>=1.10",
    ],
)
