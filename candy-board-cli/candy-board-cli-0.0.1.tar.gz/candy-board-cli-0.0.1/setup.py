#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages

version = "0.0.1"

if sys.argv[-1] == 'publish':
    # Run `setup.py register` if you get `error: Upload failed (403): You are not allowed to edit ...` message
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

setup(
    name='candy-board-cli',
    version=version,
    author='Daisuke Baba',
    author_email='baba.daisuke@gmail.com',
    url='http://github.com/CANDY-LINE/candy-board-cli',
    download_url='https://github.com/CANDY-LINE/candy-board-cli/tarball/{0}'.format(version),
    description='CANDY Board Service CLI',
    long_description=open('README.md').read() + '\n\n' + open('LICENSE').read(),
    license='BSD3',
    scripts=['bin/candy'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Hardware',
    ],
    keywords=(
        'CANDY EGG', 'CANDY LINE'
    ),
)
