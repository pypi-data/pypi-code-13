################################################################
# zopyx.plone.hyphenator
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


import json

from zope.component import getUtility
from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry

from zopyx.plone.hyphenator.interfaces import IHyphenatorSettings


class Hyphenator(BrowserView):

    def configuration(self):
        config = {}
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IHyphenatorSettings)
        config['selectors'] = settings.selectors.split('\n')
        config['minwordlength'] = settings.minwordlength
#        config['hyphenchar'] = settings.hyphenchar
        config['useCSS3hyphenation'] = settings.useCSS3hyphenation
        return json.dumps(config)
