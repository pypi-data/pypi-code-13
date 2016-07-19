# coding=utf-8

import os
import unittest

from monstro.core.constants import SETTINGS_ENVIRONMENT_VARIABLE
from monstro.core.exceptions import ImproperlyConfigured
from monstro.conf import _import_settings_class


class SettingsTest(unittest.TestCase):

    def setUp(self):
        os.environ[SETTINGS_ENVIRONMENT_VARIABLE] = (
            'monstro.conf.default.Settings'
        )

    def test_import(self):
        settings = _import_settings_class()

        self.assertTrue(settings.debug)

    def test_import__wrong(self):
        import monstro.conf.default
        monstro.conf.default.Settings.debug = ''

        with self.assertRaises(ImproperlyConfigured):
            _import_settings_class()

    def test_import__error(self):
        os.environ.pop(SETTINGS_ENVIRONMENT_VARIABLE)

        with self.assertRaises(ImproperlyConfigured):
            _import_settings_class()
