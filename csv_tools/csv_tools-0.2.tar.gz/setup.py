"""A setuptools based setup module for csv_tools"""
#!/usr/bin/env python

from codecs import open
from os import path
from setuptools import setup, find_packages

with open(path.join('.', 'README.md'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'chardet',
    'logbook'
]
test_requirements = [
    # TODO: put package test requirements here
    'pytest',
    'hypothesis'
]

setup(
    name='csv_tools',
    version=0.2,
    description="Tools for working with delimited files.",
    long_description=readme,
    author="cw-andrews",
    author_email='cwandrews.oh@gmail.com',
    url='https://github.com/cw-andrews/csv_tools',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    keywords='csv, delimited, csv_tools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='csv_tools/tests',
    tests_require=test_requirements
)
