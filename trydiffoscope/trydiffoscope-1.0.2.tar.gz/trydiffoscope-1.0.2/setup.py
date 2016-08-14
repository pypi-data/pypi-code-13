#!/usr/bin/env python3

from setuptools import setup

setup(
    name='trydiffoscope',

    url="https://chris-lamb.co.uk/projects/trydiffoscope",
    version='1.0.2',
    description="in-depth comparison of files, archives, and directories (try.diffoscope.org client)",

    author="Chris Lamb",
    author_email="lamby@debian.org",
    license="GPL-3+",

    packages=(),
    scripts=(
        'trydiffoscope',
    ),
    install_requires=(
        'requests',
    ),
)
