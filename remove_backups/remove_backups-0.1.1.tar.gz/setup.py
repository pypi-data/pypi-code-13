#!/usr/bin/env python

from setuptools import setup, find_packages

bitbucket_url = 'https://gprohorenko@bitbucket.org/gprohorenko/remove_backups'

setup(
    name='remove_backups',
    version='0.1.1',
    description='Remove old backups',
    long_description=open('README.rst', 'r').read(),
    author='blinchik',
    author_email='prohorenko_gena_@mail.ru',
    download_url='https://bitbucket.org/gprohorenko/remove_backups/downloads/remove_backups.tar.gz',
    url=bitbucket_url,
    include_package_data=True,
    license='MIT License',
    zip_safe=False,
    packages=find_packages(),
    scripts=['remove_backups.py'],
)
