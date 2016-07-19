# coding=utf-8

from gateguard import Schema, ArrayField, StringField, BooleanField, MapField


class SettingsSchema(Schema):

    secret_key = StringField()
    debug = BooleanField()
    mongodb_uri = StringField()
    mongodb_database = StringField()

    modules = ArrayField(field=StringField(), required=False, default=[])
    tornado_settings = MapField(required=False, default={})
