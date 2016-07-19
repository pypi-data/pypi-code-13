# coding=utf-8

import tornado.gen

from .db import db
from .queryset import QuerySet


class Manager(object):

    def bind(self, model):
        self.model = model

    def __getattr__(self, attribute):
        return getattr(QuerySet(self.model), attribute)

    @tornado.gen.coroutine
    def create(self, **kwargs):
        instance = yield self.model(**kwargs).save()
        yield instance.construct()
        raise tornado.gen.Return(instance)

    @tornado.gen.coroutine
    def get(self, **query):
        for key, value in query.items():
            query[key] = (
                yield self.model.__fields__[key].to_internal_value(value)
            )

        data = yield db[self.model.__collection__].find_one(query)

        if not data:
            raise self.model.DoesNotExist()

        instance = self.model(**data)
        yield instance.construct()

        raise tornado.gen.Return(instance)
