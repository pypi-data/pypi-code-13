#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'PyYAML',
    'beautifulsoup4',
    'Jinja2',
    'markdown',
    'requests'
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='wikicreator',
    version='0.3.15',
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    long_description=readme + '\n\n' + history,
    author="Matan Silver",
    author_email='matansilver@gmail.com',
    url='https://github.com/MatanSilver/wikicreator',
    packages=[
        'wikicreator',
    ],
    package_dir={'wikicreator':
                 'wikicreator'},
    entry_points={
        'console_scripts': [
            'wikicreator=wikicreator.cli:main'
        ]
    },
    data_files=[('wikicreator', ['wikicreator/data/sidebar.css', 'wikicreator/data/wikitemplate.html'])],
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='wikicreator',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        #"Programming Language :: Python :: 2",
        #'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
        #'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
