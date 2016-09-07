"""gen.subbuild.build_make

Implements a Distutils command to run make.
"""

__revision__ = "$Id$"

import os
from os.path import join as path_join, dirname, abspath, exists
from distutils.command.build import build
from distutils.core import Command
from distutils.errors import DistutilsSetupError
from distutils.sysconfig import customize_compiler
from distutils.util import execute
from distutils import log
from subprocess import call
from gen.compile import ffi

PROJECT_ROOT = dirname(dirname(abspath(__file__)))
MAKEFILE = path_join(PROJECT_ROOT, 'libfirm', 'Makefile')


def need_make(unused):
    return 'FIRM_HOME' not in os.environ and exists(MAKEFILE)

build.sub_commands.insert(0, ('build-make', need_make))


class build_make(Command):

    description = "Run make to build libraries used by Python extensions"

    user_options = [
        ('build-temp=', 't',
         "directory to put temporary build by-products"),
        ('debug', 'g',
         "compile with debugging information"),
        ('force', 'f',
         "forcibly build everything (ignore file timestamps)"),
        ('variant=', None,
         "Compile for 'debug', 'profile', 'coverage' or 'optimize' variants")
        ]

    boolean_options = ['debug', 'force']

    help_options = []

    def initialize_options(self):
        self.build_temp = None
        self.debug = None
        self.variant = None
        self.force = 0

    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('build_temp', 'build_temp'),
                                   ('debug', 'debug'),
                                   ('force', 'force'),
                                   ('variant', 'variant'))
        if not self.variant:
            self.variant = 'debug' if self.debug else 'optimize'

        self.firm_build = path_join(self.build_temp, 'libfirm')

        self.libfirm_a = path_join(self.firm_build, self.variant,
                                   'libfirm.a')
        for extension in self.distribution.ext_modules:
            self.filter_paths(extension.extra_objects)
            self.filter_paths(extension.include_dirs)

    def filter_paths(self, paths):
        subs = {'build_dir' : self.firm_build, 'variant' : self.variant}
        paths[:] = [path % subs for path in paths]

    def run(self):
        execute(self.run_make, (), "Making %s" % self.libfirm_a)

    def run_make(self):
        call(['make',
              'top_builddir=%s' % os.path.abspath(self.firm_build),
              'variant=%s' % self.variant, os.path.abspath(self.libfirm_a)],
             cwd=os.path.join(PROJECT_ROOT, 'libfirm'))
