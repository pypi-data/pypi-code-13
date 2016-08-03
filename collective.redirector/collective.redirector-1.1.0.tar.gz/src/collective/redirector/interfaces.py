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

    redirectExternalLinks = schema.Bool(
        title=(u'Enable redirect for all external links to this page.'),
        description=(u'Note: if there are more than one Redirect Page '
                     u'enabled with this feature, then it will redirect each '
                     u'link to the last created Redirect Page.'),
        default=False
    )

    enableRegexURL = schema.Bool(
        title=(u'Enable URL redirection '
               u'for links matching the given RegEx url patterns.'),
        description=(u'Enabling this feature may require you to write RegEx ('
                     u'Regular Expressions. To find out more about RegEx '
                     u'visit http://regexone.com/. \n'
                     u'Nevertheless, if you wish to redirect all external '
                     u'links to an intermediate page, you can add '
                     u'http://(?!yoursite\.com).* '
                     u'in the field below.'),
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
        required=False,
        default=u"")
    submitButtonTitle = schema.TextLine(
        title=u"Submit title",
        default=u"Accept terms and conditions")
