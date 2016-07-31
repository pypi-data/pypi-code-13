#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generic Setup script, takes package info from __pkginfo__.py file.
"""
from sys import argv
from os import listdir
from os.path import isdir, exists, join, dirname
from setuptools import setup

__docformat__ = "restructuredtext en"
base_dir = dirname(__file__)

__pkginfo__ = {}
with open(join('__pkginfo__.py')) as f:
    exec(f.read(), __pkginfo__)


def packages(directory, prefix):
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
                result += packages(absfile, result[-1])
    return result

def scripts(linux_scripts):
    """Creates the proper script names required for each platform"""
    from distutils import util
    if util.get_platform()[:3] == 'win':
        return linux_scripts + [script + '.bat' for script in linux_scripts]
    return linux_scripts


def setupkwargs(pinf):
    skwargs = {}
    uniss = (
        'author_email',
        'data_files',
        'description',
        'ext_modules',
        'install_requires',
        'license',
        'version')
    unils = (
        'classifiers',
        'dependency_links',
        'entry_points',
        'include_dirs',
        'packages',
        )
    names = {
        'modname': 'name',
        'distname': 'name',
        'long_desc': 'long_description',
        'web': 'url'}
    for uni in uniss:
        skwargs[uni] = pinf.get(uni, None)
    for uni in unils:
        skwargs[uni] = pinf.get(uni, [])
    for (key, val) in names.items():
        if key in pinf:
            skwargs[val] = pinf[key]
            if key in skwargs.keys():
                del skwargs[key]
    return skwargs

__pkginfo__['packages'] = [__pkginfo__['modname']] + \
    packages(join(base_dir, __pkginfo__['modname']), __pkginfo__['modname'])

kwargs = setupkwargs(__pkginfo__)
if '-v' in argv or '--verbose' in argv:
	print()
	for (k, v) in sorted(kwargs.items()):
		print(k, '=', v)
	print()
setup(**kwargs)
