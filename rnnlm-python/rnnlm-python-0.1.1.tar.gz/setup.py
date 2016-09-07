#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="rnnlm-python",
    version="0.1.1",
    author="Hiroki Teranishi",
    author_email="teranishihiroki@gmail.com",
    description="python wrapper for RNNLM Toolkit (http://rnnlm.org/)",
    long_description=long_description,
    url="https://github.com/chantera/rnnlm-python",
    license="MIT",
    py_modules=["rnnlm"],
    ext_modules=[
        Extension(
            "_rnnlm",
            sources=["./rnnlm-python/rnnlm_wrap.cxx", "./rnnlm/rnnlmlib.cpp"]
        )
    ],
    packages=["rnnlm-python"],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Processing :: Linguistic",
    ],
)
