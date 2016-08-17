# -*- coding: utf-8 -*-

from setuptools import setup
from phpenv import __version__

setup(
    name='phpenv',
    version = __version__,
    url='https://github.com/lomonosow/phpenv',
    license='MIT',
    author='Lomonosow',
    author_email='lomonosow93@gmail.com',
    install_requires=[],
    description='Php virtual environment builder',
    py_modules=['phpenv'],
    entry_points={
        'console_scripts': ['phpenv = phpenv:main']
    },
    zip_safe=False,
    platforms='any'
)
