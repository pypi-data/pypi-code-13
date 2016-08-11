"""
twelvefactor
============

Links
-----

* `Documentation <https://twelvefactor.readthedocs.org/>`_
* `GitHub <https://github.com/artisanofcode/python-twelvefactor>`_
"""

import ast
import re

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('twelvefactor.py', 'rb') as f:
    version = f.read().decode('utf-8')
    version = str(ast.literal_eval(_version_re.search(version).group(1)))

setup(
    name='twelvefactor',
    version=version,
    url='http://github.com/artisanofcode/python-twelvefactor',
    license='BSD',
    author='Daniel Knell',
    author_email='contact@danielknell.co.uk',
    description='Utilities for 12factor apps',
    long_description=__doc__,
    py_modules=['twelvefactor'],
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
