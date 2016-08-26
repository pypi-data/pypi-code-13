#!/usr/bin/env python3
import unittest
from distutils.core import Command, setup

import lordkey


class TestCommand(Command):
    """..."""
    user_options = list()

    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        """..."""
        loadTestsFromNames = unittest.defaultTestLoader.loadTestsFromNames
        suite = unittest.TestSuite()
        suite.addTests(loadTestsFromNames(['tests', ]))
        result = unittest.TextTestRunner(verbosity=2).run(suite)


setup(
    name='LordKey',
    version=lordkey.__version__,
    description=(
        'Detect the sequence element by identifier or '
        'the identifier by element of sequence.'
    ),
    license='MIT',
    long_description=lordkey.__doc__,
    author='Davydenko Myroslav',
    author_email='i@valsorym.com',
    packages = ['lordkey', ],
    provides = ['lordkey', ],
    cmdclass = {'test': TestCommand, },
    url = 'https://github.com/valsorym/lordkey/',
)

