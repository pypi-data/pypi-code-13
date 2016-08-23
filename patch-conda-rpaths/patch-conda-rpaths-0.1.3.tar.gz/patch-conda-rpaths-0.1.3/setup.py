from __future__ import print_function

import sys
import platform

if 'bdist_wheel' in sys.argv:
    import setuptools

from distutils.core import setup
from distutils.extension import Extension
from distutils.version import LooseVersion as V

if sys.platform != 'darwin':
    raise ValueError("Only makes sense on OS X")

with open('patch-conda-rpaths') as f:
    for line in f:
        if line.startswith('__version__'):
            __version__ = eval(line.split('=', 1)[1])
            break

setup_args = dict(
    name = "patch-conda-rpaths",
    version = __version__,
    scripts = [
        'patch-conda-rpaths'
    ],
    author = "Min Ragan-Kelley",
    author_email = "benjaminrk@gmail.com",
    url = 'http://github.com/minrk/patch-conda-rpaths',
    description = "Disable App Nap on OS X 10.9",
    long_description = """
    Patch conda dylibs with @rpath/name. Most conda packages have this,
    but some old packages not built with conda-build (python itself, mkl) don't have this,
    which causes many runtime compilation tools to fail.
    """,
    license = "MIT",
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)

setup(**setup_args)

