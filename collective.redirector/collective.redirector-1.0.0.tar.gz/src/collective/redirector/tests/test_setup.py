# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.redirector.testing import COLLECTIVE_REDIRECTPAGE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.redirector is properly installed."""

    layer = COLLECTIVE_REDIRECTPAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.redirector is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.redirector'))

    def test_browserlayer(self):
        """Test that ICollectiveRedirectLayer is registered."""
        from collective.redirector.interfaces import (
            ICollectiveRedirectLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveRedirectLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_REDIRECTPAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.redirector'])

    def test_product_uninstalled(self):
        """Test if collective.redirector is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.redirector'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveRedirectLayer is removed."""
        from collective.redirector.interfaces import ICollectiveRedirectLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveRedirectLayer, utils.registered_layers())
