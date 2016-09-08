#!/usr/bin/env python
import sys
from distutils.core import setup

from arpactor import __version__

PY3 = sys.version_info[0] == 3


_unicode = str if PY3 else unicode


setup(
    name="arpactor",
    version=_unicode(__version__),
    description="A framework to react on ARP packets from certain MAC addresses",
    long_description="",
    author="Fabian Topfstedt",
    author_email="topfstedt@schneevonmorgen.com",
    url="http://bitbucket.org/fabian/arpactor",
    license="MIT license",
    packages=["arpactor"],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
)
