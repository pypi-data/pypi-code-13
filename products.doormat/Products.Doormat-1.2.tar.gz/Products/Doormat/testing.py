# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.testing import z2
from zope.configuration import xmlconfig


class ProductsDoormatLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.Doormat
        xmlconfig.file(
            'configure.zcml',
            Products.Doormat,
            context=configurationContext
        )
        z2.installProduct(app, 'Products.Doormat')

        import plone.app.contenttypes
        xmlconfig.file(
            'configure.zcml',
            plone.app.contenttypes,
            context=configurationContext
        )

        # XXX:
        # plone.app.contenttypes needs plone.app.event, who needs this one.
        # https://github.com/plone/plone.app.event/issues/81
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.Doormat:default')
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        setRoles(portal, TEST_USER_ID, ['Manager'])

    def tearDownPloneSite(self, portal):

        # not implemented yet
        #applyProfile(portal, 'Products.Doormat:uninstall')

        # plone.app.contenttypes needs plone.app.event, who needs this one.
        # https://github.com/plone/plone.app.event/issues/81
        z2.uninstallProduct(portal, 'Products.DateRecurringIndex')


PRODUCTS_DOORMAT_FIXTURE = ProductsDoormatLayer()
PRODUCTS_DOORMAT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PRODUCTS_DOORMAT_FIXTURE, ),
    name="ProductsDoormatLayer:Integration"
)
PRODUCTS_DOORMAT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PRODUCTS_DOORMAT_FIXTURE,),
    name="ProductsDoormatLayer:Functional"
)
PRODUCTS_DOORMAT_ROBOT_TESTING = FunctionalTesting(
    bases=(PRODUCTS_DOORMAT_FIXTURE, z2.ZSERVER_FIXTURE),
    name="ProductsDoormatLayer:Robot"
)
