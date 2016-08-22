# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.i18n.normalizer.interfaces import IURLNormalizer
from Products.CMFCore.utils import getToolByName
from Products.Doormat.testing import PRODUCTS_DOORMAT_INTEGRATION_TESTING
from zope.component import queryUtility

import unittest2 as unittest

class DoormatViewTest(unittest.TestCase):
    """Test with only default doormat content."""

    layer = PRODUCTS_DOORMAT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.types = self.portal.portal_types
        self.catalog = self.portal.portal_catalog
        self.portal.invokeFactory('Folder', 'news')
        self.folder = self.portal['news']
        self.folder.invokeFactory(
            'News Item',
            'news1',
            title="News 1",
        )
        self.folder.invokeFactory(
            'News Item',
            'news2',
            title="News 2",
        )
        self.folder.invokeFactory(
            "Collection",
            "collection",
            title="New Collection",
        )
        self.news1 = self.folder['news1']
        self.news2 = self.folder['news2']
        self.collection = self.folder['collection']
        query = [{
            'i': 'Type',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'News Item',
        }]
        self.collection.setQuery(query)

    def test_collection(self):
        self.assertEqual(len([col.Title for col in self.collection.queryCatalog()]),2)
        self.assertItemsEqual([col.Title for col in self.collection.queryCatalog()],['News 1','News 2'])

    def test_doormat_view(self):
        view = self.portal.doormat.restrictedTraverse('@@doormat-view')
        view()
        query = dict(portal_type="DoormatSection")
        results = self.catalog(query)
        self.assertEqual(len(results),1)
        section = results[0].getObject()
        section.invokeFactory(
            'DoormatCollection',
            'collection1',
            title='Collection 1',
        )
        #set collection
        door_collection = section['collection1']
        door_collection.setCollection(self.collection)
        self.assertItemsEqual([col.Title for col in door_collection.getCollection().queryCatalog()],['News 1','News 2'])
        results = view.getCollection(door_collection)
        self.assertItemsEqual([item.Title for item in results],['News 1','News 2'])
        #set limit
        door_collection.setLimit(1)
        results = view.getCollection(door_collection)
        self.assertItemsEqual([item.Title for item in results],['News 1',])

    def test_replace_link_variables_by_paths_for_dx_links(self):
        # This is needed because this test is only for Dexterity: if I don't
        # make the Link type from DX available, it will use Archetypes making
        # this test useless.
        applyProfile(self.portal, 'plone.app.contenttypes:default')

        normalizer = queryUtility(IURLNormalizer)

        section = self.catalog(dict(portal_type="DoormatSection"))
        section_obj = section[0].getObject()

        # ${portal_url}
        link_title_portal_url = u'Link Portal Url'
        link_id_portal_url = normalizer.normalize(link_title_portal_url)
        link_url_portal_url = u'/plone/{0}'.format(link_id_portal_url)
        remote_url_portal_url = u'${{portal_url}}/{0}'.format(link_id_portal_url)
        section_obj.invokeFactory(
            u'Link',
            link_id_portal_url,
            title=link_title_portal_url,
            remoteUrl=remote_url_portal_url,
        )
        #

        # ${navigation_root_url}
        link_title_navigation_root_url = u'Link Navigation Root Url'
        link_id_navigation_root_url = normalizer.normalize(
            link_title_navigation_root_url
        )
        link_url_navigation_root_url = u'/plone/{0}'.format(
            link_id_navigation_root_url
        )
        remote_url_navigation_root_url = u'${{navigation_root_url}}/{0}'.format(
            link_id_navigation_root_url
        )
        section_obj.invokeFactory(
            u'Link',
            link_id_navigation_root_url,
            title=link_title_navigation_root_url,
            remoteUrl=remote_url_navigation_root_url,
        )
        #

        portal_url_ok = False
        navigation_root_url_ok = False
        view = self.portal.doormat.restrictedTraverse('@@doormat-view')
        data = view.getDoormatData()
        for column in data:
            for section in column['column_sections']:
                for link in section['section_links']:
                    if link['link_title'] == link_title_portal_url:
                        portal_url_ok = (
                            link['link_url'] == link_url_portal_url
                        )
                    if link['link_title'] == link_title_navigation_root_url:
                        navigation_root_url_ok = (
                            link['link_url'] == link_url_navigation_root_url
                        )

        self.assertTrue(portal_url_ok)
        self.assertTrue(navigation_root_url_ok)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
