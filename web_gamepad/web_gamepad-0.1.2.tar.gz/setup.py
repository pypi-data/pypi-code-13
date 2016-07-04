#!/usr/bin/env python

from distutils.core import setup

setup(
    name='web_gamepad',
    version='0.1.2',
    packages=['core', 'gamepad', 'simple_commander', 'simple_commander.game', 'simple_commander.utils'],
    package_data={'templates':['*'],'static':['*']},
    package_dir={'': 'src'},
    url='https://github.com/peterzdeb/WebGamepad',
    license='Apache License, Version 2.0',
    author='Petro Zdeb',
    author_email='peterzdeb@gmail.com',
    description='Gamepad controller library based on lightweight AsyncIO web server'
)
