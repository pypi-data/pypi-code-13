#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
VERSION = '0.1'
setup(
    name='pkulogin',
    version=VERSION,
    description="login https://its.pku.edu.cn with python",

    entry_points={
        'console_scripts':[
            'pkulogin = pkulogin:main'
        ]
    },
    include_package_data=True,
    license='MIT',
    zip_safe=True,
    author='Yue Liu',
    packages=["pkulogin"],
)