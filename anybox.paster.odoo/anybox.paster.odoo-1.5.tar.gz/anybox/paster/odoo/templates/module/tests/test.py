# coding: utf-8
from anybox.testing.openerp import SharedSetupTransactionCase


class TestSomething(SharedSetupTransactionCase):
    _module_ns = '${name}'

    @classmethod
    def initTestData(self):
        super(TestSomething, self).initTestData()
        # init tests...

    def test_something(self):
        """ explain the test in 1 line.
        """
        # write the scenario first in several steps, then write the test
        cr, uid = self.cr, self.uid
        # we do something
        self.assertTrue(True)
        # then we do something else
        # then...
        # blah blah
