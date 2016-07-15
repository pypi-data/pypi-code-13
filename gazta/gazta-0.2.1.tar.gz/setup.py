#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install
#import pkg_resources
import webbrowser

class install(_install):
    def run(self):
        try:
            _install.run(self)
            webbrowser.open('https://www.codesyntax.com/cheese')
        finally:
            print('Open https://codesyntax.com/cheese in your browser')


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'wheel>=0.29.0',   
]


setup(
    name='gazta',
    version='0.2.1',
    description="Winning a handmade Cheese",
    long_description=readme + '\n\n' + history,
    author="CodeSyntax",
    author_email='info@codesyntax.com',
    url='https://www.codesyntax.com',
    packages=[
        'gazta',
    ],
    package_dir={'gazta':
                 'gazta'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='gazta',
    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    cmdclass={'install': install},
)
