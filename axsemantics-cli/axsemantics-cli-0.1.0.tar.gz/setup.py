from codecs import open
from os import path
from setuptools import setup

setup(
    name = 'axsemantics-cli',
    version = '0.1.0',

    description = 'AXSemantics API client Commandline Interface',

    # url = 'https://github.com/axsemantics/axsemantics-cli',

    author = 'Ramon Klass',
    author_email = 'ramon.klass@ax-semantics.com',

    license = 'MIT',

    classifiers = [
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    packages = ['axsemantics_cli'],

    install_requires = [
        'axsemantics',
        'click',
        'colorama',
    ],
    entry_points='''
        [console_scripts]
        axsemantics=axsemantics_cli.main:cli
    ''',
)
