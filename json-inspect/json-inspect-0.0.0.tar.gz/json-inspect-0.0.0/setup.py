#!/usr/bin/env python

from distutils.core import setup

setup(name = 'json-inspect',
      description = 'JSON inspection command line client',
      author = 'John Murray',
      author_email = 'me@johnmurray.io',
      url = 'http://github.com/JohnMurray/json-inspect',
      packages = ['json_inspect'],
      package_dir = {'json_inspect': ''},
      scripts = ['json-inspect'],
     )
