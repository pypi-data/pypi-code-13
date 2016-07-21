# -*- coding: utf-8 -*-

import testrest
from setuptools import setup, find_packages

setup(
    name='testrest',
    version=testrest.__version__,
    description='Test framework for testing restful interfaces in python',
    long_description="Test framework for testing restful interfaces in python",
    author='oskarnyqvist',
    author_email='oskarnyqvist@gmail.com',
    url='https://github.com/oskarnyqvist/testrest',
    # license=license,
    keywords=['testing',
              'rest', ],
    packages=['testrest'], )
