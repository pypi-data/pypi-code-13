#!/usr/bin/env python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8


from setuptools import setup, find_packages
from glob import glob
import os

# strings
lib_path = '/usr/share/tuna-wrap'

# Get description from Readme file
readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme_file).read()

setup(
    name='tuna-wrap',
    version='0.1.0',
    description='Wraps Nautilus scripts for use in Thunar file manager',
    long_description=long_description,
    author='Andreas Fritz, digital.elements.li',
    author_email='tuna-wrap@projects.elements.li',
    url='http://www.digital.elements.li',
    download_url='https://pypi.python.org/pypi/tuna-wrap',
    packages=find_packages(),
    entry_points={'console_scripts':['tuna-wrap=tuna_wrap.wrap.py'], },
    include_package_data=True,
    data_files=[
                (lib_path, glob('README.rst')),
                (lib_path, glob('LICENSE')),
                ],
    keywords="Thunar Nautilus script wrapper",
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
