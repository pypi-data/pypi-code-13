#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generic Setup script, takes package info from __pkginfo__.py file.
"""
from os import listdir
from os.path import isdir, exists, join, dirname
from setuptools import setup

__docformat__ = "restructuredtext en"
base_dir = dirname(__file__)

__pkginfo__ = {}
with open("__pkginfo__.py") as f:
    exec(f.read(), __pkginfo__)

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


def ensure_scripts(linux_scripts):
    """Creates the proper script names required for each platform"""
    from distutils import util
    if util.get_platform()[:3] == 'win':
        return linux_scripts + [script + '.bat' for script in linux_scripts]
    return linux_scripts


def setupkwargs(pinf):
    skwargs = {}
    uniqs = (
        'author_email',
        'classifiers',
        'dependency_links',
        'description',
        'entry_points',
        'install_requires',
        'license',
        'version')
    diffs = {
        'distname': 'name',
        'long_desc': 'long_description',
        'web': 'url',
        'scripts': ensure_scripts,
        'packages': get_packages}
    for uni in uniqs:
        if uni in pinf.keys():
            skwargs[uni] = pinf[uni]
    for (key, val) in diffs.items():
        if key in pinf.keys():
            if isinstance(val, str):
                skwargs[val] = pinf[key]
            else:
                skwargs[key] = val(pinf[key])
    return skwargs

kwargs = setupkwargs(__pkginfo__)
setup(**kwargs)
