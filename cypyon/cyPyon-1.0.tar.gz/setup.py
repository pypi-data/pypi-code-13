#!/usr/bin/python

import sys
from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

cmdclass = { }
ext_modules = [ ]

if use_cython:
    ext_modules += [
        Extension("cyPyon", [ "cyPyon/Root.pyx" ]),
    ]
    cmdclass.update({ 'build_ext': build_ext })
else:
    ext_modules += [
        Extension("cyPyon", [ "cyPyon/Root.c" ]),
    ]

setup(
    name='cyPyon',
    packages=['cyPyon'],
    version='1.0',
    description="A parser for Python Object Notation (PYON), written in Cython.",
    author = "Darin McGill",
    author_email = "darin@x5e.com",
    url = "https://github.com/cferko/cyPyon",
    download_url = "https://github.com/cferko/cyPyon/tarball/1.0",
    keywords = ["pyon", "serialization", "parser"],
    classifiers = [],
    cmdclass = cmdclass,
    ext_modules=ext_modules
)
