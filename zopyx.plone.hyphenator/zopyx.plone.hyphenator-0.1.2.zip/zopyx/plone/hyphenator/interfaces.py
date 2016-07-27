# -*- coding: utf-8 -*-

################################################################
# zopyx.plone.hyphenator
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

from zope import schema
from zope.interface import Interface
from zopyx.plone.hyphenator.i18n import MessageFactory as _


SELECTORS = u'.plone-toolbar-container span'


class IBrowserLayer(Interface):
    """A brower layer specific to my product """


class IHyphenatorSettings(Interface):
    """ Connector settings """

    selectors = schema.Text(
        title=_(u'Selectors'),
        description=_(u'Query selectors used to hyphenate text'),
        default=SELECTORS,
        required=False
    )
