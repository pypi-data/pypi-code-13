import os
import unittest

basedir = os.path.dirname(__file__)

class Test(unittest.TestCase):
    def test_it(self):
        from .. import main
        main(['-c', os.path.join(basedir, '001', 'alembic.ini'), '--paste-global', 'interpolant=sqlite:///', 'upgrade', 'head'])
