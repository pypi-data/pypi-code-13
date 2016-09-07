# -*- coding: utf-8 -*-
"""
    Signi
    ~~~~~
    Signi service package
"""

from setuptools import setup, find_packages


setup(
    name='signi',
    version='1.0',
    url='https://github.com/puhrez/signi',
    author='Michael Perez',
    author_email='michaelp193@gmail.com',
    description="A simple DRAE definitions tool",
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    keywords=['spanish', 'español', 'rae'],
    install_requires=['lxml', 'requests'],
    entry_points = {
        'console_scripts': ['signi=signi.signi:main'],
    },
)