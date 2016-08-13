from bson import ObjectId
from datetime import datetime
from pytz import timezone, utc
from bson.errors import InvalidId
from marshmallow.fields import Field


class LagosTimezone(Field):
    """A formatted datetime/date based on the Lagos timezone.

    This datetime never deserializes datetime from clients and
    exports it's datetime localized to lagos. This is partially
    in line with the Single Time Spec in gakp-docs. The only way
    is to set missing argument or write to it on the server using
    any function that returns a naive timestamp in utc.(e.g DateTime.now)
    .
    """
    default_error_messages = {
        'invalidop': 'Deserialization is not allowed on this field',
        'invalid': 'Default value is not a valid date',
        'format': '"{input}" cannot be formatted as a datetime.',
        'utc': '"{input}" must be naive UTC timestamp'
    }
    lagos = timezone('Africa/Lagos')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.missing:
            self.dump_only = True

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        try:
            value = self.lagos.localize(value)
            return value.isoformat()
        except AttributeError:
            self.fail('format', input=value)
        except ValueError:
            self.fail('utc', input=value)

    def _deserialize(self, value, attr, data):
        if self.missing:
            if callable(self.missing):
                return self.missing()
            else:
                return self.missing
        self.fail('invalidop')

    @classmethod
    def now(cls):
        return datetime.utcnow()


class DateTime(LagosTimezone):

    @classmethod
    def now_str(cls):
        return cls.now().isoformat()


class ObjectID(Field):
    """Serializes and deserializes ObjectId strs from mongodb"""
    default_error_messages = {
        'invalid': 'Not a valid ObjectId.',
        'format': '"{input}" cannot be formatted as an ObjectId.',
    }

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        elif isinstance(value, ObjectId):
            return str(value)
        else:
            self.fail('format', input=value)

    def _deserialize(self, value, attr, obj):
        if not value:
            self.fail('invalid')
        try:
            return ObjectId(value)
        except InvalidId:
            self.fail('invalid')
