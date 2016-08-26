#!/usr/bin/env python3
import unittest
from distutils.core import Command, setup


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
    version='0.0.2',
    description=(
        'Detect the sequence element by identifier or '
        'the identifier by element of sequence.'
    ),
    license='MIT',
    long_description="""
    LordKey

    It solves the problem of determining the combination in a sequence based on
    the some alphabet with a given length, and use combination to determine the
    iteration index.


    The problem.

    There are several elements to iterate - a, b and c. How many possible
    combinations for unique enumeration if key size is 3? Or which combination
    is at the tenth iteration? Or which iteration corresponds the `acc`
    combination?

    For `abc` alphabet and 3 key size can be created the next iterations:

         0. aaa      1. aab      2. aac      3. aba      4. abb      5. abc
         6. aca      7. acb      8. acc      9. baa     10. bab     11. bac
        12. bba     13. bbb     14. bbc     15. bca     16. bcb     17. bcc
        18. caa     19. cab     20. cac     21. cba     22. cbb     23. cbc
        24. cca     25. ccb     26. ccc

    So, the maximum number of iterations - 27, for 10 iteration corresponds to
    `baa` combination and the `acc` combination - it is 7 iteration.

    """,
    author='Davydenko Myroslav',
    author_email='i@valsorym.com',
    packages = ['lordkey', ],
    provides = ['lordkey', ],
    cmdclass = {'test': TestCommand, },
    url = 'https://github.com/valsorym/lordkey/',
)

