import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()



NAME = "venus"

PACKAGES = ["venus",]

DESCRIPTION = "This is a package of micro service architecture."

LONG_DESCRIPTION = read("README.rst")

KEYWORDS = "service"

AUTHOR = "dy"

AUTHOR_EMAIL = "email"

URL = "https://pypi.python.org/pypi/venus"

VERSION = "0.0.1"

LICENSE = "MIT"

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
)
