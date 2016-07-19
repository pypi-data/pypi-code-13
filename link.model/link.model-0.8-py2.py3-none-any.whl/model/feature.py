# -*- coding: utf-8 -*-

from b3j0f.conf import Configurable, category, Parameter
from inspect import getmembers, isroutine

from link.middleware.core import Middleware
from link.feature import Feature

from link.model import CONF_BASE_PATH


@Configurable(
    paths='{0}/base.conf'.format(CONF_BASE_PATH),
    conf=category(
        'MODEL',
        Parameter(name='schema_uri_template')
    )
)
class ModelFeature(Feature):

    name = 'model'

    def resolve_schema(self, schemaname):
        uri = self.schema_uri_template.format(schema=schemaname)
        mid = Middleware.get_middleware_by_uri(uri)

        return mid.get()

    def create_model(self, schema):
        raise NotImplementedError()

    def __call__(self, schemaname):
        schema = self.resolve_schema(schemaname)
        model = self.create_model(schema)
        return lambda **kwargs: model(schemaname, self.middleware, **kwargs)


class Model(object):
    _DATA_ID = 'id'

    def __init__(self, schemaname, middleware, **kwargs):
        super(Model, self).__init__()

        self._schemaname = schemaname
        self._middleware = middleware

        for key in kwargs:
            self[key] = kwargs[key]

    def __getitem__(self, attr):
        try:
            val = getattr(self, attr)

        except AttributeError:
            raise KeyError('Key {0} not found'.format(attr))

        return val

    def __setitem__(self, attr, val):
        setattr(self, attr, val)

    def __delitem__(self, attr):
        try:
            delattr(self, attr)

        except AttributeError:
            raise KeyError('Key {0} not found'.format(attr))

    def __contains__(self, attr):
        result = True

        try:
            getattr(self, attr)

        except AttributeError:
            result = False

        return result

    def keys(self):
        return [
            name
            for name, _ in getmembers(self, lambda m: not isroutine(m))
            if name[0] != '_'
        ]

    def __iter__(self):
        return iter(self.keys())

    def __str__(self):
        d = {
            k: self[k]
            for k in self.keys()
        }

        return str(d)

    def __repr__(self):
        return 'Model(data_id={0})'.format(self[self._DATA_ID])

    def save(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()
