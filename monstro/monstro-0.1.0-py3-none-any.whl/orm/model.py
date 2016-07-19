# coding=utf-8

import collections

import tornado.gen

from . import manager, exceptions, db
from .fields import Field, IDField


class MetaModel(type):

    @classmethod
    def __prepare__(mcs, *args, **kwargs):
        return collections.OrderedDict()

    def __new__(mcs, name, bases, attributes):
        if '_id' in attributes:
            raise AttributeError('Field "_id" reserved')

        attributes['_id'] = IDField(required=False)
        attributes.move_to_end('_id', last=False)

        fields = collections.OrderedDict()

        for parent in bases:
            if hasattr(parent, '__fields__'):
                fields.update(parent.__fields__)

        for name, field in attributes.items():
            if isinstance(field, Field):
                fields[name] = field

        for field in fields:
            attributes.pop(field, None)

        cls = type.__new__(mcs, name, bases, attributes)

        cls.__fields__ = fields
        cls.ValidationError = exceptions.ValidationError

        if attributes['__collection__'] is not None:
            cls.objects = attributes.get('objects', manager.Manager())
            cls.objects.bind(model=cls)

        cls.DoesNotExist = exceptions.DoesNotExist

        for name, field in cls.__fields__.items():
            field.bind(name=name, model=cls)

        return cls


class Model(object, metaclass=MetaModel):

    __collection__ = None

    def __init__(self, **kwargs):
        self.__values__ = kwargs
        self.__cursor__ = self.__collection__ and db.db[self.__collection__]

    def __getattr__(self, attribute):
        if attribute in self.__fields__:
            field = self.__fields__[attribute]
            return self.__values__.get(attribute, field.default)

        raise AttributeError(attribute)

    def __setattr__(self, attribute, value):
        if attribute in self.__fields__:
            self.__values__[attribute] = value
            return

        return super().__setattr__(attribute, value)

    @tornado.gen.coroutine
    def construct(self):
        for name, field in self.__fields__.items():
            value = self.__values__.get(name, field.default)

            self.__values__[name] = yield field.to_representation(value)

    @tornado.gen.coroutine
    def validate(self):
        errors = {}

        for name, field in self.__fields__.items():
            try:
                value = self.__values__.get(name, field.default)
                yield field.validate(value, self)
            except exceptions.ValidationError as e:
                errors[name] = e.error

        if errors:
            raise exceptions.ValidationError(errors)

    @tornado.gen.coroutine
    def to_internal_value(self):
        data = {}

        for name, field in self.__fields__.items():
            value = self.__values__.get(name, field.default)
            data[name] = yield field.to_internal_value(value)

        raise tornado.gen.Return(data)

    @tornado.gen.coroutine
    def save(self):
        yield self.validate()

        data = yield self.to_internal_value()
        data.pop('_id')

        if self._id:
            yield self.__cursor__.update({'_id': self._id}, data)
        else:
            self.__values__['_id'] = yield self.__cursor__.insert(data)

        raise tornado.gen.Return(self)

    @tornado.gen.coroutine
    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.__values__[key] = value

        yield self.save()

    @tornado.gen.coroutine
    def refresh(self):
        if self._id:
            data = yield self.__cursor__.find_one({'_id': self._id})

            self.__values__.update(data)

            yield self.construct()

    @tornado.gen.coroutine
    def delete(self):
        if self._id:
            yield self.__cursor__.remove({'_id': self._id})


class Choice(object):

    """Choice model.

    choices = Choice(
        ('NAME1', 'value1' 'Description NAME1'),
        ('NAME2', 'value2', 'Description NAME2'),
    )
    choices.NAME1
    >>> value1
    choices.choices
    >>> (('value1', 'Description NAME1'), ('value2', 'Description NAME2'))
    """

    __keys = ('name', 'value', 'description')

    def __init__(self, *args):
        self.__data = collections.OrderedDict()

        for item in args:
            item = dict(zip(self.__keys, item))
            self.__data[item['name']] = (item['value'], item['description'])

    def __getattr__(self, name):
        try:
            return self.__data[name][0]
        except KeyError:
            raise AttributeError(name)

    def __contains__(self, key):
        return key in self.values

    @property
    def choices(self):
        return self.__data.values()

    @property
    def values(self):
        return [choice[0] for choice in self.choices]
