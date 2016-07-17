#!/usr/bin/python
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

PACKAGE = "django-pages-cache"
NAME = "django-pages-cache"
DESCRIPTION = "Django package memcache util"
AUTHOR = "SHENOISZ"
AUTHOR_EMAIL = "marcelo.net.system@gmail.com"
URL = "https://github.com/SHENOISZ/django-pages-cache"
VERSION = __import__("pages_cache").__version__

setup(
    name=NAME,
    packages = find_packages(),
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.rst"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    # packages=["tests.*", "tests"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    keywords = [
        "cache", "memcache", "memcached", "pages cache", "django cache"
        ],
)
