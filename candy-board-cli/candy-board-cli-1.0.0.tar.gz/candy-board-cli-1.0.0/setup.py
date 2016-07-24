#!/usr/bin/env python

import os
import sys
import pypandoc
from setuptools import setup, find_packages

version = "1.0.0"

if sys.argv[-1] == 'publish':
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
    long_description=pypandoc.convert('README.md', 'rst'),
    license='BSD3',
    scripts=['bin/candy'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
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
