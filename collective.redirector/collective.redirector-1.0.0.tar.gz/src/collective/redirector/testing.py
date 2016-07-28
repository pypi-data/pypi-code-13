# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.redirector


class CollectiveRedirectpageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.redirector)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.redirector:default')


COLLECTIVE_REDIRECTPAGE_FIXTURE = CollectiveRedirectpageLayer()


COLLECTIVE_REDIRECTPAGE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_REDIRECTPAGE_FIXTURE,),
    name='CollectiveRedirectpageLayer:IntegrationTesting'
)


COLLECTIVE_REDIRECTPAGE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_REDIRECTPAGE_FIXTURE,),
    name='CollectiveRedirectpageLayer:FunctionalTesting'
)


COLLECTIVE_REDIRECTPAGE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_REDIRECTPAGE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveRedirectpageLayer:AcceptanceTesting'
)
