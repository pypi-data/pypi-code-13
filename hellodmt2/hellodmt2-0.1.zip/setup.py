#!/usr/bin/env
try:
    from setuptools import setup
except importError:
    from distutils.core import setup

setup(name = "hellodmt2",
      description = "a source distribution test",
      version = "0.1",
      author = "David",
      author_email = "dmt257257@gmail.com",
      py_modules = ["hellodmt2"],
      url = "https://github.com/dmt257/hellodmt2",
      download_url = "https://github.com/dmt257/hellodmt2/archive/0.1.zip",
      keywords = ["testing"],
      
      )
      
