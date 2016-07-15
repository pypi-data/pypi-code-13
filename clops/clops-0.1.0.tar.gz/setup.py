"""Provide metadata for Clops.

Copyright 2016 Dana Scott

This file is part of Clops.

Clops is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your
option) any later version.

Clops is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License
along with Clops. If not, see <http://www.gnu.org/licenses/>.

"""
import setuptools


def _long_description(start='Installation'):
    """Return lines from README.txt.

    Specifically, return the lines after and including the first line
    that starts with the value of start.

    """
    lines = []
    save = False
    with open('README.txt', encoding='utf_8') as f:
        for line in f:
            if save:
                lines.append(line)
            elif line.startswith(start):
                # Save the start line.
                lines.append(line)
                save = True
    return ''.join(lines)


setuptools.setup(
    name='clops',
    version='0.1.0',
    author='Dana Scott',
    author_email='danawscott0@gmail.com',
    description='A Python library to parse command line options.',
    long_description=_long_description(),
    url='https://bitbucket.org/danawscott/clops',
    license=('License :: OSI Approved :: '
             'GNU General Public License v3 or later (GPLv3+)'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Utilities',
    ],
    keywords='cli options',
    packages=setuptools.find_packages(),
)
