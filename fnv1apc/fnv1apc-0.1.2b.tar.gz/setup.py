#!/usr/bin/env python

from distutils.core import setup, Extension

fnv1apc_module = Extension('_fnv1apc',
                           sources=['fnv1apc_wrap.c', 'fnv1apc.c'],
                           )

setup (name = 'fnv1apc',
       version = '0.1.2b',
       author = 'zhangyet',
       author_email = 'zhangyet@gmail.com',
       url = 'https://github.com/ZhangYet/fnv1apc',
       description = '''pure c fnv1a_32 implement.''',
       ext_modules = [fnv1apc_module],
       py_modules = ['fnv1apc'],
       )
