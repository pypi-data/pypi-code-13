import os
from setuptools import setup, find_packages

# with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    # README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = "django-secretkey",
    version = "0.1",
    packages = find_packages(),

    scripts = [
        "cmd/secretkey",
        ],

    author = "Yeison Cardona",
    author_email = "yeisoneng@gmail.com",
    maintainer = "Yeison Cardona",
    maintainer_email = "yeisoneng@gmail.com",

    #url = "http://www.pinguino.cc/",
    url = "http://yeisoncardona.com/",
    download_url = "https://bitbucket.org/yeisoneng/python-secretkey/downloads",


    include_package_data=True,
    license = "BSD License",
    description = "Secret key generator for Django.",
    # long_description = README,
    #author = "Yeison Cardona",
    #author_email = "yeisoneng@gmail.com",
    classifiers = [
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
