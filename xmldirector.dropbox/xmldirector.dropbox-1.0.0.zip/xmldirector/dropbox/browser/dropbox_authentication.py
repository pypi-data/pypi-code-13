# -*- coding: utf-8 -*-

################################################################
# xmldirector.dropbox
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


from dropbox import session

from zope.component import getUtility
from zope.interface import alsoProvides
from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from plone.protect.interfaces import IDisableCSRFProtection
from zope.annotation import IAnnotations

from xmldirector.dropbox.interfaces import IDropboxSettings


DROPBOX_TOKEN_KEY = 'xmldirector.dropbox.token_key'
DROPBOX_TOKEN_SECRET = 'xmldirector.dropbox.token_secret'
DROPBOX_TEMP_TOKEN = 'xmldirector.dropbox.oauth_temporary_token'


class DropboxAuthentication(BrowserView):

    def __init__(self, context, request):
        # fuck all Plone protection shit!
        alsoProvides(request, IDisableCSRFProtection)
        super(DropboxAuthentication, self).__init__(context, request)

    def authorize(self, oauth_token):
        annotation = IAnnotations(self.context)
        s = self.dropbox_session
        a = s.obtain_access_token(annotation[DROPBOX_TEMP_TOKEN])
        annotation[DROPBOX_TOKEN_KEY] = a.key
        annotation[DROPBOX_TOKEN_SECRET] = a.secret

        self.context.plone_utils.addPortalMessage(u'Dropbox access authorized')
        self.request.response.redirect(
            self.context.absolute_url() + '/authorize-dropbox')

    def deauthorize(self):
        annotation = IAnnotations(self.context)
        try:
            del annotation[DROPBOX_TOKEN_KEY]
        except KeyError:
            pass

        try:
            del annotation[DROPBOX_TOKEN_SECRET]
        except KeyError:
            pass

        self.context.plone_utils.addPortalMessage(
            u'Dropbox access deauthorized')
        self.request.response.redirect(
            self.context.absolute_url() + '/authorize-dropbox')

    @property
    def dropbox_settings(self):
        registry = getUtility(IRegistry)
        return registry.forInterface(IDropboxSettings)

    @property
    def dropbox_session(self):
        settings = self.dropbox_settings
        return session.DropboxSession(
            settings.dropbox_app_key,
            settings.dropbox_app_secret,
            'dropbox')

    def get_oauth_token(self):
        annotation = IAnnotations(self.context)
        return annotation.get(DROPBOX_TOKEN_KEY)

    def get_oauth_url(self):
        s = self.dropbox_session
        t = s.obtain_request_token()
        IAnnotations(self.context)[DROPBOX_TEMP_TOKEN] = t
        authorize_url = s.build_authorize_url(
            t, self.context.absolute_url() + '/authorize-dropbox-action')
        return authorize_url
