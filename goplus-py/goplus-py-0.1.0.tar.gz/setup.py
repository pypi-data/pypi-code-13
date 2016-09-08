import codecs
import os

from setuptools import setup, find_packages

###################################################################

PACKAGES = find_packages(where="src")
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

DESCRIPTION = "Python SDK for GOPLUSPLATFORM"

###################################################################

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


if __name__ == "__main__":
    setup(
        name='goplus-py',
        description=DESCRIPTION,
        license='Apache Software License',
        url='http://goplusplatform.com/',
        version='0.1.0',
        author='Go Plus Platform',
        author_email='info@goplusplatform.com',
        maintainer='Go Plus Platform',
        maintainer_email='info@goplusplatform.com',
        keywords='goplus iot platform sdk',
        long_description=read("README.rst"),
        packages=PACKAGES,
        package_dir={"": "src"},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=["paho-mqtt", "requests"],
        extras_require={
            'rpi': ['RPi.GPIO'],
        })
