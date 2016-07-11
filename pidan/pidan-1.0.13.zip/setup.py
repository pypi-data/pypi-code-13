# install:python setup.py sdist upload
# -*- coding:utf-8 -*-
from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.13',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = u'http模块增加get_params_from_url 从url获取查询参数的函数，修正了create_url函数url不能带参数的问题',
    package_data = {
        '': ['*.data'],
    },
)