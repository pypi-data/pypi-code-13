from datetime import datetime

from plone.app.layout.viewlets import ViewletBase
from plone import api
from zope.component import ComponentLookupError
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getMultiAdapter
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.api.exc import InvalidParameterError
from collective.redirector.interfaces import (IRedirect, schema_prefix,
                                                TESTDATA)

from time import time
from plone.memoize import ram


class JSFunctionsViewlet(ViewletBase):
	pass


class RedirectViewlet(ViewletBase):
    """ viewlet that displays announcements """

    def redirect_span(self, obj):
        return ("<span class='collective-redirect-data' data-external-redirect='{3}' "
                "data-redirect='{0}' data-url='{1}' data-regex='{2}'></span>").format(
            obj.redirectURL or "",
            obj.absolute_url(),
            "*" if obj.enableRegexURL else "^",
            'true' if obj.redirectExternalLinks else 'false'
        )

    @property
    def redirect_to(self):
        return "policy-confirmation"

    @property
    def prefix(self):
        return schema_prefix

    def is_front_page(self):
        """
        Check if the viewlet is on a front page.
        Handle canonical paths correctly.
        based on docs:
        http://docs.plone.org/develop/plone/serving/traversing.html#checking-if-an-item-is-the-site-front-page
        """
        # Get path with "Default content item" wrapping applied
        context_helper = getMultiAdapter((self.context, self.request),
                                                 name="plone_context_state")
        canonical = context_helper.canonical_object()
        path = canonical.absolute_url_path()
        return INavigationRoot.providedBy(canonical)

    # @ram.cache(lambda *args: time() // (60 * 60))
    def redirects(self):
        """Get the list of RedirectPage objects from portal_catalog."""
        catalog = api.portal.get_tool('portal_catalog')
        redirects = catalog(portal_type='RedirectPage') #review_state="published"
        results = []
        obj = {}
        for redirect in redirects:
            redirect = redirect.getObject()
            obj = dict(
                enableRedirect=redirect.enableRedirect,
                redirectURL=redirect.redirectURL,
                span=self.redirect_span(redirect)
            )
            results.append(obj)
        return results
