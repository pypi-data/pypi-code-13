# -*- coding: utf-8 -*-
"""
:Authors: cykooz
:Date: 11.07.2016
"""
from __future__ import unicode_literals

import logging
import os
import subprocess
import sys


class Extension(object):

    def __init__(self, buildout):
        self.buildout = buildout
        self.parts_dir = buildout['buildout']['parts-directory']
        venv_dir = os.path.join(self.parts_dir, 'venv')
        self.venv_dir = buildout['buildout'].get('venv-directory', venv_dir)
        self._logger = logging.getLogger('zc.buildout')

    def __call__(self):
        if not os.path.isdir(self.venv_dir):
            self._logger.info('Install virtual python environment...')
            if sys.version_info < (3, 3):
                self.create_by_virtualenv(self.venv_dir)
            else:
                self.create_by_venv(self.venv_dir)
            self._logger.info('Virtual python environment was installed.')

        executable = os.path.join(self.venv_dir, 'bin', 'python')

        if executable != sys.executable:
            self._logger.info('Recreating buildout script.')
            args = sys.argv[:]
            bootstrap_args = [executable, args[0], 'bootstrap']
            subprocess.call(bootstrap_args)
            self._logger.info('Restarting buildout under virtual python environment.')
            args.insert(0, executable)
            sys.exit(subprocess.call(args))

    def create_by_virtualenv(self, venv_path):
        from virtualenv import create_environment
        create_environment(venv_path, no_setuptools=True, no_pip=True, no_wheel=True)

    def create_by_venv(self, venv_path):
        from venv import create
        create(venv_path, symlinks=True)


def extension(buildout=None):
    return Extension(buildout)()
