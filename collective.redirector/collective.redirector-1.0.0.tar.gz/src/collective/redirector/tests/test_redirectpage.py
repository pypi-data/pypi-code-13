# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from collective.redirector.testing import COLLECTIVE_REDIRECTPAGE_INTEGRATION_TESTING  # noqa
from collective.redirector.interfaces import IRedirect

import unittest2 as unittest


class RedirectPageIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_REDIRECTPAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='RedirectPage')
        schema = fti.lookupSchema()
        self.assertEqual(IRedirect, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='RedirectPage')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='RedirectPage')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IRedirect.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('RedirectPage', 'RedirectPage')
        self.assertTrue(
            IRedirect.providedBy(self.portal['RedirectPage'])
        )
