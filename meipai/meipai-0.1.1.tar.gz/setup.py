#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: PyBeaner
# @Date:   2016-07-21 22:08:33
# @Last Modified by:   PyBeaner
# @Last Modified time: 2016-07-22 23:36:21


from setuptools import setup, find_packages

setup(
    name='meipai',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'BeautifulSoup4',
    ],

    entry_points={
        'console_scripts': [
            'meipai = src:start'
        ],
    },

    author='PyBeaner',
    author_email='758046738@qq.com',
    url='https://github.com/PyBeaner/meipai',
    description='A command line interface to search,play videos on meipai',
    keywords=['meipai', 'video', 'cli'],
    license='MIT'
)
