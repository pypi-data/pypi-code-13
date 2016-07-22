# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-07 11:43:23
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-22 10:10:27


from distutils.core import setup
from setuptools import Extension,find_packages
from os import path

setup(
    name = 'digpe',
    version = '0.1.1',
    description = 'extract price from text',
    author = 'Lingzhe Teng',
    author_email = 'zwein27@gmail.com',
    url = 'https://github.com/ZwEin27/phone-price-extractor',
    download_url = 'https://github.com/ZwEin27/phone-price-extractor/tarball/0.1.1',
    packages = find_packages(),
    keywords = ['price', 'extractor'],
    install_requires=['digSparkUtil']
)