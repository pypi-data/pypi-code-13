import codecs
import os
import sys
 
try:
    from setuptools import setup
except:
    from distutils.core import setup
# from setuptools import setup, find_packages


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
 

NAME = "dj-kits"

 
PACKAGES = ["dj_kits", "dj_kits.autocomplete_light", 'dj_kits.decorators', 'dj_kits.magicpages', 'dj_kits.templatetags', 'dj_kits.utils']

 
DESCRIPTION = "this is a test package for packing django liberaries tutorial."

 
LONG_DESCRIPTION = "hello, this is a test package for packing django liberaries tutorial."

 
KEYWORDS = "django"

 
AUTHOR = "Carol_cn"

 
AUTHOR_EMAIL = "Carol_8955@163.com"

 
 
VERSION = "1.0.3"

 
LICENSE = "MIT"


URL = "http://pypi.python.org/"


setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'Unidecode'
    ],
    platforms = 'any',
    url = URL
)
