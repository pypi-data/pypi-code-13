#!/usr/bin/env python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8


from setuptools import setup, find_packages
from glob import glob
import os
import shutil
import sys


# strings
HOME = os.environ['HOME']
lib_path = '%s/.local/share/photo-namer-nautilus' % HOME

# Get description from Readme file
readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme_file).read()

setup(
    name='photo-namer-nautilus',
    version='0.0.4',
    description='Photo namer nautilus file manager script for files imported with CatGrab phpto import app.',
    long_description=long_description,
    author='Andreas Fritz, digital.elements.li',
    author_email='photo-namer@projects.elements.li',
    url='http://www.digital.elements.li',
    download_url='https://pypi.python.org/pypi/photo-namer-nautilus',
    packages=find_packages(),
    include_package_data=True,
    scripts=["data/photo_namer.py"],
    data_files=[
                (lib_path, glob('README.rst')),
                (lib_path, glob('LICENSE')),
                ],
    keywords="photo namer script file manager nautilus thunar nemo",
    classifiers=[
                'Development Status :: 4 - Beta',
                'License :: OSI Approved :: MIT License',
                'Operating System :: Unix',
                'Programming Language :: Python :: 3',
                'Environment :: Console',
                'Natural Language :: English',
                'Intended Audience :: End Users/Desktop',
                'Topic :: Desktop Environment',
                'Topic :: Desktop Environment :: File Managers',
                'Topic :: Desktop Environment :: Gnome'
                ],
    )

bins = '%s/.local/bin/photo_namer.py' % HOME
nscript = '%s/.local/share/nautilus/scripts/PHOTO-NAMER' % HOME
if not sys.argv[1] == 'sdist':
    if os.path.isfile(bins):
        shutil.copy(bins, nscript)


