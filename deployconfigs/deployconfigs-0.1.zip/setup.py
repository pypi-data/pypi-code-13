# -*- coding:utf-8 -*-
'''
Created on Mar 7, 2016

@author: Wasim
'''

from setuptools import setup


setup(
    name='deployconfigs',
    description='A centerilized place to handle deploy configs',
    url='https://github.com/tsaze/deployconfigs',
    author='wtayyeb',
    author_email='wtayyeb@gmail.com',
    license='MIT',
    py_modules=["deployconfigs", ],
    use_scm_version=True,
    install_requires=[
        'dj-database-url',
        'django-cache-url',
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',# ??
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',# ??
        # 'Programming Language :: Python :: 3.3',# ??
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
