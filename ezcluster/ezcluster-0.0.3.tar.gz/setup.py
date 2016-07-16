#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import re
import sys
from subprocess import PIPE, run

try:
    import pypandoc
    readme = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    readme = ''


package = 'ezcluster'
requirements = [

]
test_requirements = [

]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


def get_author(package):
    """
    Return package author as listed in `__author__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__author__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


def get_email(package):
    """
    Return package email as listed in `__email__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__email__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


# python setup.py register
if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    args = {'version': get_version(package)}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()

prev_tag = run("git tag", shell=True, stdout=PIPE, universal_newlines=True).stdout[:-1]
run("git tag -d " + prev_tag, shell = True)
run("git push --delete origin " + prev_tag, shell = True)
command = "git tag -a " + get_version(package) + " -m 'version " + get_version(package) + "'"
run(command, shell = True)
run("git push --tags", shell = True)

setup(
    name='ezcluster',
    version=get_version(package),
    description='Evaluating the optimal number of clusters for KMeans clustering using the gap statistic',
    long_description=readme,
    author=get_author(package),
    author_email=get_email(package),
    url='https://github.com/thisisandreeeee/ezcluster',
    download_url='https://github.com/thisisandreeeee/ezcluster/tarball/' + get_version(package),
    packages=[
        'ezcluster'
    ],
    package_dir={'ezcluster': 'ezcluster'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords=['kmeans', 'clustering', 'gap statistic', 'unsupervised learning', 'machine learning'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
