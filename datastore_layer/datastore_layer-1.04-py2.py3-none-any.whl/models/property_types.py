# see https://cloud.google.com/appengine/docs/python/datastore/typesandpropertyclasses
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop


class PropertyTypes:
    def __init__(self):
        pass

    Integer, Float, Boolean, String, Text, Blob, BlobKey, Date, Time, DateTime, GeoPt, Key, Enum = range(13)


def create_property(property_type, repeated=False, required=False, default=None, auto_now=False, kind=None,
                    auto_now_add=False, enumClass=None, indexed=False, choices=None):
    if property_type == PropertyTypes.Integer:
        return ndb.IntegerProperty(repeated=repeated, required=required, default=default)
    if property_type == PropertyTypes.Float:
        return ndb.FloatProperty(repeated=repeated, required=required, default=default)
    if property_type == PropertyTypes.Boolean:
        return ndb.BooleanProperty(repeated=repeated, required=required, default=default)
    if property_type == PropertyTypes.String:
        return ndb.StringProperty(repeated=repeated, required=required, default=default)
    if property_type == PropertyTypes.Text:
        return ndb.TextProperty(repeated=repeated, required=required, default=default)
    if property_type == PropertyTypes.Blob:
        return ndb.BlobProperty(repeated=repeated, required=required, default=default)
    if property_type == PropertyTypes.BlobKey:
        return ndb.BlobKeyProperty(repeated=repeated, required=required, default=default)
    if property_type == PropertyTypes.Date:
        return ndb.DateProperty(repeated=repeated, required=required, default=default,
                                auto_now=auto_now, auto_now_add=auto_now_add)
    if property_type == PropertyTypes.Time:
        return ndb.TimeProperty(repeated=repeated, required=required, default=default,
                                auto_now=auto_now, auto_now_add=auto_now_add)
    if property_type == PropertyTypes.DateTime:
        return ndb.DateTimeProperty(repeated=repeated, required=required, default=default,
                                    auto_now=auto_now, auto_now_add=auto_now_add)
    if property_type == PropertyTypes.GeoPt:
        return ndb.GeoPtProperty(repeated=repeated, required=required, default=default)
    if property_type == PropertyTypes.Key:
        return ndb.KeyProperty(repeated=repeated, required=required, default=default, kind=kind)
    if property_type == PropertyTypes.Enum:
        return msgprop.EnumProperty(enumClass, required=required, indexed=indexed, choices=choices)
