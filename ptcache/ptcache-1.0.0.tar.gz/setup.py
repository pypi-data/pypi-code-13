"""
Tornado route
    :copyright: (c) 2016 by fangpeng(@beginman.cn).
    :license: MIT, see LICENSE for more details.
"""
import re
import os

from setuptools import setup, find_packages


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


def desc():
    info = read("README.md")
    try:
        return info + '\n\n' + read('doc/changelog.rst')
    except IOError:
        return info


# grep tornado_route/__init__.py since python 3.x cannot import it before using 2to3
file_text = read(fpath('ptcache/__init__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


setup(
    name="ptcache",
    version=grep("__version__"),
    url="",
    license='BSD',
    author=grep('__author__'),
    author_email=grep('__email__'),
    description='Simple and extensible cache for python.',
    long_description=desc(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        "redis"
    ]
)


