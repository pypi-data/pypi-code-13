"""Setuptools based setup module for docker-rerun."""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='docker-rerun',

    version='0.1.1',

    description='Command-line tool to re-run a docker container',

    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',

    url='https://github.com/csmith/docker-rerun',

    author='Chris Smith',
    author_email='chris87@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    keywords='docker container',

    py_modules=["docker_rerun"],

    install_requires=[],

    test_suite='nose.collector',

    extras_require={
        'dev': [],
        'test': ['coverage', 'nose', 'pylint'],
    },

    entry_points={
        'console_scripts': [
            'docker-rerun=docker_rerun:main',
        ],
    },
)

