import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ipfinder",
    version = "0.2",
    author = "Joshua Yabut",
    author_email = "yabut.joshua@gmail.com",
    description = ("Simple library to grab an external IP using HTTPS."),
    requires = ["requests"],
    license = "BSD",
    keywords = "iplookup ip find whois",
    url = "http://packages.python.org/ipfinder",
    py_modules=['ipfinder'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
