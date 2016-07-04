#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup pel la llibreria de Exportació dels 1048.
"""
import os
import sys
import shutil

from setuptools import setup
from distutils.command.clean import clean as _clean

from libcnmc1048 import __version__

PACKAGES = ['libcnmc1048']
PACKAGES_DATA = {}


def find_scripts():
    _scripts = []
    for r, d, f in os.walk('bin'):
        if len(f):
            for _f in f:
                _scripts.append('bin/' + _f)
    return _scripts


class Clean(_clean):
    """Eliminem el directori build i els bindings creats."""
    def run(self):
        """Comença la tasca de neteja."""
        _clean.run(self)
        if os.path.exists(self.build_base):
            print "Cleaning %s dir" % self.build_base
            shutil.rmtree(self.build_base)

INSTALL_REQUIRES = ['progressbar', 'libComXML']
if sys.version_info[1] < 6:
    INSTALL_REQUIRES += ['multiprocessing']

setup(name='libcnmc1048',
      description='Scripts per el CNMC 1048',
      author='GISCE Enginyeria',
      author_email='devel@gisce.net',
      url='http://www.gisce.net',
      version=__version__,
      license='General Public Licence 2',
      long_description='''Long description''',
      provides=['libcnmc1048'],
      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES,
      package_data=PACKAGES_DATA,
      scripts=find_scripts(),
      cmdclass={'clean': Clean})
