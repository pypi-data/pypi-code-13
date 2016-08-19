#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
import sys, os
"""
打包的用的setup必须引入
"""

VERSION = '0.0.4'

with open('README.rst') as f:
    long_description = f.read()

setup(
      name='savemd', # 文件名
      version=VERSION, # 版本(每次更新上传Pypi需要修改)
      description="Conver a html to markdown.",
      long_description=long_description, # 放README.md文件,方便在Pypi页展示
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='markdown html convert', # 关键字
      author='laixintao', # 用户名
      author_email='laixintao1995@163.com', # 邮箱
      url='https://github.com/laixintao/savemd', # github上的地址,别的地址也可以
      license='MIT', # 遵循的协议
      packages=['savemd'], # 发布的包名
      include_package_data=True,
      zip_safe=True,
      install_requires=[

      ], # 满足的依赖
      entry_points={
        'console_scripts':[
            'savemd = savemd:main'
        ]
      },
)