# coding=utf-8

import unittest

from . import imports


class ImportObjectTest(unittest.TestCase):

    def test_import_module(self):
        import datetime
        module = imports.import_object('datetime')

        self.assertEqual(datetime, module)

    def test_import_object(self):
        import monstro.management.commands.run
        module = imports.import_object(
            'monstro.management.commands.run.execute'
        )

        self.assertEqual(monstro.management.commands.run.execute, module)

    def test_import_module__error(self):
        with self.assertRaises(ImportError):
            imports.import_object('dtetime')

    def test_import_object__error(self):
        with self.assertRaises(ImportError):
            imports.import_object('datetime.wrong')
