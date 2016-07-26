#!/usr/bin/env python
# coding=utf-8
#
# Author:
# Created Time: 2016年07月26日 星期二 11时02分41秒

from setuptools import setup, find_packages

setup(
    name='sofc',
    version='0.1.5',
    keywords=('stackoverflow'),
    description='stackoverflow client for quick search',
    license='MIT License',

    url='https://cyy0523xc.github.io/',
    author='Alex Cai',
    author_email='cyy0523xc@gmail.com',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=["click", "pyquery", "requests"],
    scripts=["sofc/sofc.py"],
    entry_points={
        "console_scripts": [
            'sofc = sofc.sofc:main'
        ]
    }
)
