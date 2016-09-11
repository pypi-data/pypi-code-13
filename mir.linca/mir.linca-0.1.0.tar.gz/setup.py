#!/usr/bin/env python3

from setuptools import setup

setup(
    name='mir.linca',
    version='0.1.0',
    description='Link new files in watched directory elsewhere.',
    long_description='',
    keywords='',
    url='https://github.com/darkfeline/mir.linca',
    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.5',
    ],

    py_modules=['mir.linca'],
    entry_points={
        'console_scripts': [
            'linca = mir.linca:main',
        ],
    },
)
