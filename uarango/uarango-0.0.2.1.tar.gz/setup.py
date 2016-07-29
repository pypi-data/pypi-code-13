# -*- coding: utf8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'uarango',
    'description': 'UNIST arangoDB Restful Python Library',
    'author': 'Kyunghoon Kim',
    'author_email': 'preware@gmail.com',
    'url': 'https://github.com/koorukuroo/uarango',
    'version': '0.0.2.1',
    'classifiers': ['Programming Language :: Python :: 2.7', 'Topic :: Database', 'Development Status :: 5 - Production/Stable'],
    'install_requirements': ['nose', 'requests', 'json', 'uuid'],
    'packages': ['uarango'],
    'scripts': [],
    'include_package_data': True,
    'package_data': {'': ['assets/*.txt']}
}

setup(**config)
