#!/usr/bin/env python


from codecs import open
from os import path
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['test.py']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='flatter',
    version='0.0.1',
    description="Sequence flattener",
    long_description='',
    url='https://github.com/pelotoncycle/cycle_detector',
    author='Adam DePrince',
    author_email='adam@pelotoncycle.com',
    license='Apache',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    py_modules=['flatter'],
    install_requires=['six'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage', 'pytest', 'pytest-cov', 'flake8'],
    },
    cmdclass={'test': PyTest},
)
