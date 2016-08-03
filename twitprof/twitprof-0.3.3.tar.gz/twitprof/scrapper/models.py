# coding: utf-8
import datetime
from mongoengine import Document, StringField, DateTimeField, IntField, connect


def connect_to_database(database_name, **kwargs):
    connect(db=database_name, **kwargs)


class TwitterUser(Document):
    _id = IntField(primary_key=True)
    screen_name = StringField(required=True, max_length=100)
    name = StringField(required=True, max_length=200)
    description = StringField(required=False)
    image_url = StringField(required=True)
    popularity = IntField(required=True)
    updated = DateTimeField(default=datetime.datetime.now)
