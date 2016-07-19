# coding=utf-8

import unittest

from . import imports


class ImportObjectTest(unittest.TestCase):

    def test_import_module(self):
        import datetime
        module = imports.import_object('datetime')

        self.assertEqual(datetime, module)

    def test_import_object(self):
        import datetime
        module = imports.import_object('datetime.datetime.now')

        self.assertEqual(datetime.datetime.now, module)

    def test_import_module__error(self):
        with self.assertRaises(ImportError):
            imports.import_object('dtetime')

    def test_import_object__error(self):
        with self.assertRaises(ImportError):
            imports.import_object('datetime.wrong')
