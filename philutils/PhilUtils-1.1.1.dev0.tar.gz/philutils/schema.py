from __future__ import print_function
from datetime import date


class MappingMeta(type):
    def __new__(cls, name, parents, attributes):
        if name != 'Mapping':
            if 'key_type' not in attributes:
                message = 'key_type attribute required on Mapping classes'
                raise ValueError(message)
            if 'value_type' not in attributes:
                message = 'value_type attribute required on Mapping classes'
                raise ValueError(message)
            if not isinstance(attributes['key_type'], type):
                raise TypeError('the key_type attribute should be a type')
            if not isinstance(attributes['value_type'], type):
                raise TypeError('the value_type attribute should be a type')

        def repr_method(self):
            return 'Mapping %s -> %s' % (
                self.key_type.__name__,
                self.value_type.__name__)

        def init_method(self):
            self._items = dict()

        def iter_method(self):
            for item in self._items.__iter__():
                yield item

        def len_method(self):
            return self._items.__len__()

        def getitem_method(self, key):
            return self._items[key]

        def setitem_method(self, key, value):
            if not isinstance(key, self.key_type):
                template = 'key was supposed to be a %s but you sent a %s'
                raise TypeError(template % (self.key_type, type(key)))
            elif not isinstance(value, self.value_type):
                template = 'value was supposed to be a %s but you sent a %s'
                raise TypeError(template % (self.value_type, type(value)))
            else:
                self._items[key] = value

        final_object_attributes = dict()
        final_object_attributes['__repr__'] = repr_method
        final_object_attributes['__init__'] = init_method
        final_object_attributes['__iter__'] = iter_method
        final_object_attributes['__len__'] = len_method
        final_object_attributes['__getitem__'] = getitem_method
        final_object_attributes['__setitem__'] = setitem_method
        for key, value in attributes.items():
            final_object_attributes[key] = value

        return super(MappingMeta, cls).__new__(
            cls, name, parents, final_object_attributes)


Mapping = MappingMeta(str('Mapping'), (), {})

class DocumentMeta(type):
    def __new__(cls, name, parents, attributes):
        def repr_method(self):
            repr_strings = []
            for key, value in self._fields.items():
                repr_strings.append('%s = %s' % (key, repr(value)))
            return '\nDocument %s:\n    ' % name + '\n    '.join(repr_strings)

        def init_method(self, **kwargs):
            for key, value in kwargs.items():
                if key in self._fields:
                    self._fields[key].__set__(self, value)

        def check_for_key_existance(self, key):
            if key not in self._fields:
                raise AttributeError("'%s' has no attribute '%s'" % (
                    self.__class__.__name__,
                    key))

        def getattr_method(self, key):
            check_for_key_existance(self, key)
            return self._fields[key].__get__(self)

        def setattr_method(self, key, value):
            check_for_key_existance(self, key)
            self._fields[key].__set__(self, value)

        def getitem_method(self, name):
            return self._fields[name].__get__(self)

        final_object_attributes = dict()
        final_object_attributes['__repr__'] = repr_method
        final_object_attributes['__init__'] = init_method
        final_object_attributes['__getattr__'] = getattr_method
        final_object_attributes['__setattr__'] = setattr_method
        final_object_attributes['__getitem__'] = getitem_method

        fields = dict()
        for key, value in attributes.items():
            if isinstance(value, BaseField):
                fields[key] = value
            else:
                final_object_attributes[key] = value
        final_object_attributes['_fields'] = fields
        return super(DocumentMeta, cls).__new__(
            cls, name, parents, final_object_attributes)


Document = DocumentMeta(str('Document'), (), {})


class BaseField(object):
    def __init__(self, **kwargs):
        self._required = kwargs.get('required', False)
        self._value = None
        if 'default' in kwargs:
            self._set_value(kwargs['default'])

    def __get__(self, document_object, objtype=None):
        return self._value

    def __set__(self, document_object, value):
        self._set_value(value)

    def _set_value(self, value):
        if callable(value):
            value = value()
        self.validate_value(value)
        self._value = value

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            repr(self._value))

    def validate_value(self, value):
        raise NotImplementedError


class PrimitiveTypeField(BaseField):
    value_type = object

    def validate_value(self, value):
        if not isinstance(value, self.value_type):
            message = '%s may only contain %s objects but %s is a %s' % (
                self.__class__.__name__,
                self.value_type.__name__,
                repr(value),
                type(value).__name__)
            raise TypeError(message)


class IntegerField(PrimitiveTypeField):
    value_type = int


class StringField(PrimitiveTypeField):
    value_type = str


class DateField(PrimitiveTypeField):
    value_type = date

class DocumentField(PrimitiveTypeField):
    value_type = Document
