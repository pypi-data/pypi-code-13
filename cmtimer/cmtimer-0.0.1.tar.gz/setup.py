#!/usr/bin/env python

from setuptools import setup

meta = {
    'name': 'cmtimer',
    'version': '0.0.1',
    'py_modules': ('cmtimer',),
    'tests_require': (
        'flake8-print',
        'flake8-todo',
        'pep8-naming',
        'pytest',
        'pytest-benchmark',
        'pytest-flake8',
        'pytest-isort',
        'pytest-readme'
    ),
    'description': "A simple context manager timing utility.",
    'long_description': open('README.rst').read(),
    'author': "Wojtek Ruszczewski",
    'author_email': "python@wr.waw.pl",
    'url': "http://github.org/wrwrwr/cmtimer",
    'license': "MIT",
    'classifiers': (
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    )
}

if __name__ == '__main__':
    setup(**meta)
