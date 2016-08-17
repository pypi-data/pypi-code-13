#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'json-inspect',
    version = '0.1.4',

    author = 'John Murray',
    author_email = 'me@johnmurray.io',
    description = 'JSON inspection command line client',
    license='Apache 2.0',
    package_dir = {'json_inspect': ''},
    packages = ['json_inspect'],
    scripts = ['json-inspect'],
    url = 'http://github.com/JohnMurray/json-inspect',
 )
