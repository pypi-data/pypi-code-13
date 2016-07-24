from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from setuptools import setup, find_packages


VERSION = "0.1.0"


def read(fname):
    return open(fname).read()


setup(
    name="multitude",
    version=VERSION,
    author="Chuck Bassett",
    author_email="iamchuckb@gmail.com",
    description="A couple of useful data structures",
    license="MIT",
    url="https://github.com/chucksmash/multitude.git",
    keywords="directed graph ordered set structures",
    packages=find_packages(exclude=["tests"]),
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
