#!/usr/bin/env python

"""Setup script for Dots."""

import setuptools

from dots import __project__, __version__

try:
    README = open("readme.rst").read()
    CHANGELOG = open("docs/changes.rst").read()
except IOError:
    LONG_DESCRIPTION = "<placeholder>"
else:
    LONG_DESCRIPTION = README + '\n' + CHANGELOG

setuptools.setup(
    name=__project__,
    version=__version__,

    description="Linux System Manager.",
    url='https://github.com/hoytnix/dots',
    author='Michael Hoyt',
    author_email='dots@hoyt.io',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': ['dots=dots.cli:main']},

    long_description=LONG_DESCRIPTION,
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Unix Shell',
        'Topic :: Desktop Environment',
        'Topic :: System :: Boot :: Init',
        'Topic :: System :: Installation/Setup',
        'Topic :: Utilities'
    ],

    install_requires=open("requirements.txt").readlines(),
)
