#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generic Setup script, takes package info from __pkginfo__.py file.
"""
from __future__ import absolute_import, print_function

from os import listdir
from os.path import isdir, exists, join, dirname

import sys
import shutil

from setuptools import setup

__docformat__ = "restructuredtext en"
base_dir = dirname(__file__)
__pkginfo__ = {}
with open(join(base_dir, "pwclip", "__pkginfo__.py")) as f:
    exec(f.read(), __pkginfo__)
modname = __pkginfo__['modname']
distname = __pkginfo__.get('distname', modname)
scripts = __pkginfo__.get('scripts', [])
data_files = __pkginfo__.get('data_files', None)
include_dirs = __pkginfo__.get('include_dirs', [])
ext_modules = __pkginfo__.get('ext_modules', None)
install_requires = __pkginfo__.get('install_requires', None)
dependency_links = __pkginfo__.get('dependency_links', [])
readme_path = join(base_dir, 'README')
if exists(readme_path):
    with open(readme_path) as stream:
        long_description = stream.read()
else:
    long_description = ''

def ensure_scripts(linux_scripts):
    """Creates the proper script names required for each platform"""
    from distutils import util
    if util.get_platform()[:3] == 'win':
        return linux_scripts + [script + '.bat' for script in linux_scripts]
    return linux_scripts


def get_packages(directory, prefix):
    """return a list of subpackages for the given directory"""
    result = []
    for package in listdir(directory):
        absfile = join(directory, package)
        if isdir(absfile):
            if exists(join(absfile, '__init__.py')):
                if prefix:
                    result.append('%s.%s' % (prefix, package))
                else:
                    result.append(package)
                result += get_packages(absfile, result[-1])
    return result



def install(**kwargs):
    """setup entry point"""
    packages = [modname] + get_packages(join(base_dir, 'pwclip'), modname)
    kwargs['install_requires'] = install_requires
    kwargs['dependency_links'] = dependency_links
    kwargs['entry_points'] = {'console_scripts': [
        'pwclip = pwclip:pwclipper']}
    kwargs['packages'] = packages
    return setup(name=distname,
                 version=__pkginfo__['version'],
                 license=__pkginfo__['license'],
                 description=__pkginfo__['description'],
                 long_description=long_description,
                 author=__pkginfo__['author'],
                 author_email=__pkginfo__['author_email'],
                 url=__pkginfo__['web'],
                 scripts=ensure_scripts(scripts),
                 classifiers=__pkginfo__['classifiers'],
                 data_files=data_files,
                 ext_modules=ext_modules,
                 **kwargs)

if __name__ == '__main__':
    install()
