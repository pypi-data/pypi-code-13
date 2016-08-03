from plone.dexterity.browser.view import DefaultView
from plone import api

from collective.redirector.interfaces import schema_prefix


class RedirectView(DefaultView):
    """ This is the redirectview see the configure.zcml"""

    def original_url(self):
        return self.request.form.get("original_url", "")

    @property
    def prefix(self):
        return schema_prefix
