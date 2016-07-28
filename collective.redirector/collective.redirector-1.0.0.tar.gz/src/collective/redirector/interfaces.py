# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.redirector import _
from zope import schema
from zope.interface import Interface
from plone.directives import form
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveRedirectLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

schema_prefix = \
    "collective.redirector.interfaces.IRedirect"

TESTDATA = {
    "policyMessage": "",
    "submitButtonTitle": "Accept terms and conditions",
    "redirectURL": "https://bookings.sita.aero/itd/itd/oj/Air",
    "enableRedirect": False
}


class IRedirect(Interface):
    """ Define settings data structure """

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    enableRedirect = schema.Bool(
        title=u'Enable URL redirection.',
        default=False,
        required=False,
    )

    form.widget(body=WysiwygFieldWidget)
    body = schema.Text(
        title=u"Page Body",
        default=u"This is a page redirection")

    enableRegexURL = schema.Bool(
        title=(u'Enable URL redirection '
               u'starting with the given urls.'),
        default=False,
        required=False,
    )
    redirectURL = schema.Text(
        title=u"Redirect URL",
        description=(u"For multiple urls, separate each url by a space or a "
                     u"new line. "
                     u"Note: if redirection is enabled, then all requests "
                     u"to the given url will be redirected to this "
                     u"page before continuing to the given url."),
        default=u"")
    submitButtonTitle = schema.TextLine(
        title=u"Submit title",
        default=u"Accept terms and conditions")
