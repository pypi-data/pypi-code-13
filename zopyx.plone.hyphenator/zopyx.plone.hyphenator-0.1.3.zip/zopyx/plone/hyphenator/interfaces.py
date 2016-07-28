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
    
    minwordlength = schema.Int(
        title=_(u'Minimum word length'),
        description=_(u'Only hyphenate words longer than N characters'),
        default=6,
        required=True
    )
    
#    hyphenchar = schema.TextLine(
#        title=_(u'Hyphenation character'),
#        description=_(u'Character used as hyphenation character'),
#        default=u"\u00AD", # soft hyphen
#        required=True
#    )
    
    useCSS3hyphenation = schema.Bool(
        title=_(u'Use CSS3 browser hyphenation if available (JS fallback otherwise)'),
        default=True,
    )
