"""odtlib utilities

:organization: Logilab
:copyright: 2008-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
from contextlib import contextmanager
import tempfile
import shutil

@contextmanager
def tempdir():
    try:
        path = tempfile.mkdtemp()
        yield path
    finally:
        shutil.rmtree(path)


