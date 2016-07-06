# install:python setup.py sdist upload
# -*- coding:utf-8 -*-
from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.12',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = u'http模块增加get_post_params函数，获取post的参数字符串信息',
    package_data = {
        '': ['*.data'],
    },
)