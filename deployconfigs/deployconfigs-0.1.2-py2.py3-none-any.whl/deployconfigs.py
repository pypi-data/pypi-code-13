"""
    DeployConfigs
"""

import os

import dj_database_url
import django_cache_url


try:
    import configparser
    BOOLEAN_STATES = dict(configparser.RawConfigParser.BOOLEAN_STATES)  # force copy
except ImportError:
    import ConfigParser as configparser
    BOOLEAN_STATES = dict(configparser.RawConfigParser._boolean_states)  # force copy

try:  # no strict dependency on django. in case it exist we use exceptions from it
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    class ImproperlyConfigured(Exception):
        pass


DEFAULT_ENV = 'DJANGO_CONF'
DEFAULT_SECTION = 'DJANGO'
TEST_SECTION = 'TEST'


def as_boolean(val):
    return BOOLEAN_STATES.get(str(val)) is True


class DeployConfigs(object):

    def __init__(self, env=DEFAULT_ENV, section=DEFAULT_SECTION, required=None, check_environ=True):
        self.env = env
        self.section = section
        self.required = required or []
        self.check_environ = check_environ

        self.ready = False

    def _configure(self):
        DJANGO_CONF = os.environ.get(self.env)
        if DJANGO_CONF is None:
            raise ImproperlyConfigured('Please set `%s` environment' % self.env)

        self.cf = configparser.ConfigParser()
        self.cf.read(DJANGO_CONF)
        self.ready = True

    def get(self, option, default=None, section=None, check_environ=None):
        if not self.ready:
            self._configure()

        if check_environ is None:
            check_environ = self.check_environ

        # let environment overwrite what is in\or not in the conf file.
        if check_environ and section is None:
            val = os.environ.get(option, Undefined)
            if val is not Undefined:
                return val
        try:
            return self.cf.get(section or self.section, option)

        except configparser.NoOptionError as e:
            if option in self.required:
                raise e
            return default

    def getboolean(self, option, default=False, section=None, check_environ=None):
        if not self.ready:
            self._configure()

        if check_environ is None:
            check_environ = self.check_environ

        if check_environ and section is None:
            val = os.environ.get(option, Undefined)
            if val is not Undefined:
                return as_boolean(val)

        try:
            return self.cf.getboolean(section or self.section, option)
        except configparser.NoOptionError:
            return default

    def database_dict(self, option='DATABASE_URL', conn_max_age=0, default=None, section=None):
        section = section or self.section
        return dj_database_url.parse(self.get(option, section=section) or default, conn_max_age=conn_max_age)

    database_url = database_dict

    def cache_dict(self, option='CACHE_URL', default='locmem://', section=None):
        section = section or self.section
        return django_cache_url.parse(self.get(option, section=section) or default)

    cache_url = cache_dict


class LazyList(object):
    """ LazyList used for changable list accross sub-settings
        change it to list or tuple when no change will occure
    """
    def __init__(self, *args):
        self._list = list(args[:])

    def __iter__(self):
        return iter(self._list)

    def __add__(self, other):
        assert isinstance(other, (list, tuple))
        self._list.extend(other)
        return self

    def __radd__(self, other):
        assert isinstance(other, (list, tuple))
        self._list = list(other) + self._list
        return self

    def __str__(self, *args, **kwargs):
        return str(self._list)

    def __len__(self):
        return len(self._list)

    def index(self, value):
        return self._list.index(value)

    def insert(self, index, object_):
        self._list.insert(index, object_)


class Undefined(object):
    pass
