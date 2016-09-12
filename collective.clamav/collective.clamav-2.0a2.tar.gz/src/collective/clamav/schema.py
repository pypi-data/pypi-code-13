# -*- coding: utf-8 -*-
from archetypes.schemaextender.interfaces import ISchemaModifier
from Products.ATContentTypes.interfaces import IATFile
from Products.ATContentTypes.interfaces import IATImage
from zope.component import adapts
from zope.interface import implements


class VirusFreeModifier(object):
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema[self.fieldname].validators.appendRequired('isVirusFree')


class VirusFreeFileModifier(VirusFreeModifier):
    adapts(IATFile)
    fieldname = 'file'


class VirusFreeImageModifier(VirusFreeModifier):
    adapts(IATImage)
    fieldname = 'image'
