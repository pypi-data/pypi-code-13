#!/usr/bin/env python
 
from distutils.core import setup
from distutils.extension import Extension

setup(name="pyecm2cue",
    version="1.0",
    description="",
    author="Ferdinand Silva",
    author_email="ferdinandsilva@ferdinandsilva.com",
    url="https://github.com/six519/pyecm2cue",
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
		'Programming Language :: C',
		'Programming Language :: C++',
        'License :: Freeware',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    download_url="https://github.com/six519/pyecm2cue",
    ext_modules=[
        Extension("pyecm2cue", 
            sources = ["unecm.cpp"]
        )
    ]
)