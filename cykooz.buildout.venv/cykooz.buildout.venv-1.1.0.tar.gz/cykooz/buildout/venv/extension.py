# -*- coding: utf-8 -*-
"""
:Authors: cykooz
:Date: 11.07.2016
"""
from __future__ import unicode_literals

import logging
import platform
import subprocess
import sys
from os.path import join, isfile, abspath


PY_LESS_33 = sys.version_info < (3, 3)


class Extension(object):

    def __init__(self, buildout):
        self.buildout = buildout
        self.parts_dir = buildout['buildout']['parts-directory']
        venv_dir = join(self.parts_dir, 'venv')
        self.venv_dir = buildout['buildout'].get('venv-directory', venv_dir)
        self.is_win = platform.system() == 'Windows'
        if self.is_win:
            self.venv_python_path = abspath(join(self.venv_dir, 'Scripts', 'python.exe'))
        else:
            self.venv_python_path = abspath(join(self.venv_dir, 'bin', 'python'))
        self._logger = logging.getLogger('zc.buildout')

    def __call__(self):
        if not isfile(self.venv_python_path):
            self._logger.info('Installing virtual python environment...')
            if PY_LESS_33:
                self.create_by_virtualenv()
            else:
                self.create_by_venv()
            self._logger.info('Virtual python environment was installed.')

        if self.venv_python_path != sys.executable:
            self._logger.info('Recreating buildout script.')
            args = sys.argv[:]
            bootstrap_args = [self.venv_python_path, args[0], 'bootstrap']
            subprocess.call(bootstrap_args)
            self._logger.info('Restarting buildout under virtual python environment.')
            args.insert(0, self.venv_python_path)
            sys.exit(subprocess.call(args))

    def create_by_virtualenv(self):
        from virtualenv import create_environment
        create_environment(self.venv_dir, no_setuptools=True, no_pip=True, no_wheel=True,
                           symlink=not self.is_win)

    def create_by_venv(self):
        from venv import create
        create(self.venv_dir, symlinks=not self.is_win)


def extension(buildout=None):
    return Extension(buildout)()
