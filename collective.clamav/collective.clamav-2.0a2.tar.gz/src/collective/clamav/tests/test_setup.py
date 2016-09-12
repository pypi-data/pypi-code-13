# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.clamav.testing import COLLECTIVE_CLAMAV_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.clamav is properly installed."""

    layer = COLLECTIVE_CLAMAV_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.clamav is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.clamav'))

    def test_browserlayer(self):
        """Test that ICollectiveClamavLayer is registered."""
        from collective.clamav.interfaces import (
            ICollectiveClamavLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveClamavLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_CLAMAV_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.clamav'])

    def test_product_uninstalled(self):
        """Test if collective.clamav is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.clamav'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveClamavLayer is removed."""
        from collective.clamav.interfaces import ICollectiveClamavLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveClamavLayer, utils.registered_layers())
