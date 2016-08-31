"""Some common features to simplify datastore integration."""


from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import app_identity

import uuid
import datetime
import hashlib


def md5(*text):
    checksum = hashlib.md5(text[0])
    for t in text[1:]:
        checksum.update(t)
    return checksum.hexdigest()


def uuid_namespace(kind):
    """The UUID namespace for a particular model."""
    is_kind_type = (type(kind) is type(ndb.Model))  # noqa
    if is_kind_type and issubclass(kind, ndb.Model):
        kind = kind._get_kind()
    hostname = app_identity.get_default_version_hostname()
    modelspace = '%s.%s' % (kind, hostname)
    return uuid.uuid5(uuid.NAMESPACE_DNS, modelspace)


def generate_key(kind, **props):
    """Construct a UUID as a key identifier."""
    now = datetime.datetime.now()
    props['$now'] = now.strftime('%Y%m%d-%H:%M:%S.%f')
    props = md5(*['%s:%r' for (k, v) in props.items()])
    return str(uuid.uuid5(uuid_namespace(kind), props))


class UUIDKeyModel(ndb.Model):
    """
    Provide UUID vectors instead of the default NDB key definition.

    This can be particularly helpful if key identifiers may otherwise contain
    sensitive data, or if many key identifiers need to be transmitted outside
    the datastore itself (e.g. to a web front-end). The UUID composition hides
    any sensitive components of the default ID, and is safe to transmit in many
    other environments.
    """

    def __key__(self):
        """Construct a key proactively, with a UUID model."""
        if self._key is None:
            kind = self._get_kind()
            props = self.to_dict()
            self._key = ndb.Key(kind, generate_key(kind, **props))
        return self._key

    def _put_async(self, **ctx_options):
        self.__key__()
        return super(UUIDKeyModel, self)._put_async(**ctx_options)

    def __init__(self, *args, **kwargs):
        """Prepare the model with a UUID key."""
        _key, _id = kwargs.pop('key', None), kwargs.pop('id', None)
        if _key is None and _id is None:
            kind = self._get_kind()
            _key = ndb.Key(kind, generate_key(kind, **kwargs),
                           parent=kwargs.pop('parent', None),
                           app=kwargs.pop('app', None),
                           namespace=kwargs.pop('namespace', None)
                           )

        if (not _key) and _id:
            kwargs['id'] = _id
        elif (_key):
            kwargs['key'] = _key
        return super(UUIDKeyModel, self).__init__(*args, **kwargs)


class InheritedKeysModel(ndb.Model):
    """Simple utilities for handling ancestor relationships."""

    @property
    def descendant_keys(self):
        """Iterator of all descendant entities (by key)."""
        return ndb.Query(ancestor=self.key).iter(keys_only=True)

    def delete_recursive(self):
        """Remove this entry plus all children."""
        children = list(self.descendant_keys)
        ndb.delete_multi(children + [self.key])


class UserReference(InheritedKeysModel, UUIDKeyModel):
    """User details, because NDB no longer provides."""

    userid = ndb.StringProperty(required=True, indexed=True)
    email = ndb.StringProperty(required=True, indexed=True)

    @classmethod
    def for_user(cls, user):
        assert isinstance(user, users.User), "Expects a users.User instance"
        inst = cls.query(cls.userid == user.user_id()).get()
        if inst is None:
            inst = cls(userid=user.user_id(), email=user.email())
            inst.put()
        return inst

    @property
    def user_instance(self):
        return users.User(email=self.email)

    @classmethod
    def by_email(cls, email):
        return cls.for_user(users.User(email=email))

    @classmethod
    def current(cls):
        user = users.get_current_user()
        if user is None:
            return None
        return cls.for_user(user)


class UserProperty(ndb.StructuredProperty):
    """Compose a property of User identity model."""

    def __init__(self, **options):
        self.auto_add = options.pop('auto_current_user_add', False)
        self.auto_current = options.pop('auto_current_user', False)
        return super(UserProperty, self).__init__(UserReference, **options)

    def _validate(self, value):
        assert isinstance(value, UserReference)

    def _prepare_for_put(self, entity):
        write_current_new = self.auto_add and not self._has_value(entity)
        write_current_update = self.auto_current and self._has_value(entity)
        write_current = (write_current_update or write_current_new)

        if write_current:
            value = UserReference.current()
            if value is not None:
                self._store_value(entity, value)

    def _to_base_type(self, value):
        if isinstance(value, users.User):
            return UserReference.for_user(value)
        return value

    def _from_base_type(self, value):
        return value.user_instance

    @classmethod
    def current(cls):
        return UserReference.current()


class BooleanOptionsProperty(ndb.BooleanProperty):
    """Simple boolean state for true-ish values."""

    TRUEISH = ["true", "True", "ON", "on", "checked", "enabled"]

    def __init__(self, *args, **kwargs):
        self.options = kwargs.pop('options', self.TRUEISH)
        return super(BooleanOptionsProperty, self).__init__(*args, **kwargs)

    def _validate(self, value):
        if value in (True, False):
            return value
        return (value in self.options)


class TimestampModel(ndb.Model):
    """Standard properties for tracking time of last update."""

    created_by = UserProperty(auto_current_user_add=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    updated_at = ndb.DateTimeProperty(auto_now=True, indexed=True)


class UserProfile(ndb.Expando, ndb.Model):
    """Simple user-heirarchy model."""

    preferences = ndb.PickleProperty(default={})

    @classmethod
    def current(cls):
        return cls.for_user(users.get_current_user())

    @classmethod
    def for_user(cls, user):
        user_ref = UserReference.for_user(user)
        return cls(parent=user_ref.key)


# For export, standard model
Model = type("Model", (InheritedKeysModel,), {})
