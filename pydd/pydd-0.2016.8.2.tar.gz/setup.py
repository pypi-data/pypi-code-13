#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name="pydd",
    version="0.2016.8.2",
    url='https://poncki.pl/',
    license="""don't know not yet, MIT probably""",
    author='poncki',
    author_email='pydd@poncki.pl',
    description="asorted tools for development and debugging",
    long_description="""soon...""",
    packages=find_packages('src',
                           exclude=['vendor', 'docs', 'tests', '.__stash__']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    entry_points="""
        [console_scripts]
        pyddc=pydd.cli:main
    """,
    install_requires=[
        'click',
        'colorama',
    ],
    tests_require = [
        'pytest',
        'tox',
        'pytest-pylint',
        'pytest-flake8',
    ],
    #test_suite = "tests.get_tests",
)
