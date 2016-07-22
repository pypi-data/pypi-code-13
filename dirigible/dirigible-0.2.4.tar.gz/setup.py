#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    history = readme = readme_file.read()

requirements = ['six', 'pycrypto']

test_requirements = requirements + ['pytest-cov', 'pytest-runner']

setup(
    name='dirigible',
    version='0.2.4',
    description="Config encryption",
    long_description=readme + '\n\n' + history,
    author="Thom Neale",
    author_email='tneale@massmutual.com',
    url='https://github.org/massmutual/dirigible',
    packages=find_packages(),
    package_dir={'dirigible': 'dirigible'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='dirigible',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=requirements + test_requirements,
    setup_requires=["pytest-runner"],
)
