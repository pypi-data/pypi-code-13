import os
import re
import sys

__version__ = '0.1.2'

__all__ = ('ConfigError', 'Config', 'config')


UNSET = object()


if sys.version_info[0] == 3:
    text_type = str
else:
    text_type = unicode  # NOQA


class ConfigError(Exception):
    """Exception to throw on configuration errors."""


class Config(object):
    """Config environment parser.

    This class allows chosen configuration values to be extracted from the
    processes environment variables and converted into the relevant types.

    .. code-block:: python

        parser = Config()

        config = parser({
            'DEBUG': {
                'type': bool,
                'default': False,
            },
            'SECRET_KEY': str,
        })

    The above will populate the :code:`config` variable with two values,
    :code:`DEBUG` will be populated with a :class:`bool` from the environment
    variable of the same  name, throwing an exception on invalid values and
    defaulting to :data:`False` when none is provided, and :code:`SECRET_KEY`
    will be a :class:`str` and throw a :exc:`ConfigError` when no value is
    found in the environment.

    An optional :code:`environ` param can be  passed in order to override the
    environment.

    :param environ: environment dictionary, defaults to :data:`os.environ`
    :type environ: dict

    """
    TRUE_STRINGS = ('t', 'true', 'on', 'ok', 'y', 'yes', '1')

    TEMPLATE = re.compile(r'{{([A-Z0-9_]+)}}')

    def __init__(self, environ=None):
        self.environ = environ if environ is not None else os.environ

    def __call__(self, schema):
        """Parse the environment according to a schema.

        :param schema: the schema to parse
        :type schema: dict
        :return: a dictionary of config values
        :rtype: dict

        """
        result = {}

        for key, kwargs in schema.items():
            if callable(kwargs):
                kwargs = {'type_': kwargs}
            else:
                kwargs = kwargs.copy()

            if 'type' in kwargs:
                kwargs['type_'] = kwargs.pop('type')

            if 'key' not in kwargs:
                kwargs['key'] = key

            result[key] = self.get(**kwargs)

        return result

    def parse(self, value, type_=text_type, subtype=text_type):
        """Parse value from string.

        Convert :code:`value` to

        .. code-block:: python

           >>> parser = Config()
           >>> parser.parse('12345', type_=int)
           <<< 12345
           >>>
           >>> parser.parse('1,2,3,4', type_=list, subtype=int)
           <<< [1, 2, 3, 4]

        :param value: string
        :type value: str
        :param type\_: the type to return or factory function
        :type type\_: type
        :param subtype: subtype for iterator types
        :type subtype: str
        :return: the parsed config value
        :rtype: object

        """
        if type_ is bool:
            value = value.lower() in self.TRUE_STRINGS
        if isinstance(type_, type) and issubclass(type_, (list, tuple, set)):
            value = [self.parse(v.strip(' '), subtype)
                     for v in value.split(',') if value]

        try:
            return type_(value)
        except ValueError as e:
            raise ConfigError(*e.args)

    def get(self, key, default=UNSET, type_=text_type, subtype=text_type,
            mapper=None):
        """Parse a value from an environment variable.

        .. code-block:: python

           >>> os.environ['FOO']
           <<< '12345'
           >>>
           >>> os.environ['BAR']
           <<< '1,2,3,4'
           >>>
           >>> 'BAZ' in os.environ
           <<< False
           >>>
           >>> parser = Config()
           >>> parser.get('FOO', type_=int)
           <<< 12345
           >>>
           >>> parser.get('BAR', type_=list, subtype=int)
           <<< [1, 2, 3, 4]
           >>>
           >>> parser.get('BAZ', default='abc123')
           <<< 'abc123'
           >>>
           >>> parser.get('FOO', type_=int, mapper=lambda x: x*10)
           <<< 123450

        :param key: the key to look up the value under
        :type key: str
        :param default: default value to return when when no value is present
        :type default: object
        :param type\_: the type to return or factory function
        :type type\_: type
        :param subtype: subtype for iterator types
        :type subtype: type
        :param mapper: a function to post-process the value with
        :type mapper: callable
        :return: the parsed config value
        :rtype: object

        """
        value = self.environ.get(key, UNSET)

        if value is UNSET and default is UNSET:
            raise ConfigError('Unknown environment variable: {0}'.format(key))

        if value is UNSET:
            value = default
        else:
            value = self.parse(value, type_, subtype)

        if mapper:
            value = mapper(value)

        return value


config = Config()
