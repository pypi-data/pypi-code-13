import os
import json
import toml
from typing import Mapping, T


class ConfigurationError(Exception):
    pass


class Map(dict, Mapping[str, T]):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in list(arg.items()):
                    if isinstance(v, dict):
                        v = Map(v)
                    self[k] = v

        if kwargs:
            for k, v in list(kwargs.items()):
                if isinstance(v, dict):
                    v = Map(v)
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        if isinstance(value, dict):
            value = Map(value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


formats = Map()
formats.toml = 'toml'
formats.json = 'json'


class ConfigMap(Map):
    def __init__(self, filename: str=None, *args, **kwargs):
        if filename:
            self.load(filename=filename)
        else:
            super(Map, self).__init__(*args, **kwargs)

    def load(self, filename=None):
        if self.filename and filename:
            raise ConfigurationError('Configuration file already loaded')
        elif not self.filename and not filename:
            raise ConfigurationError('No configuration file supplied')
        else:
            self.filename = filename

        config = None
        with open(self.filename) as cfg_file:
                try:
                    config = toml.loads(cfg_file.read())
                except:
                    pass
                try:
                    config = json.loads(cfg_file.read())
                except:
                    pass
        if not config:
            raise ConfigurationError(('Configuration format is unknown '
                                      'or contains an error'))
        super(Map, self).__init__(config)

    def save(self, filename: str=None, format: str=None):
        if self.filename and filename:
            raise ConfigurationError('Configuration file already loaded')
        elif not self.filename and not fname:
            raise ConfigurationError('No configuration file supplied')
        else:
            self.filename = filename

        if format == 'toml':
            with open(self.filename) as f:
                return toml.dump(self, f)
        elif format == 'json':
            with open(self.filename) as f:
                return json.dump(self, f, skipkeys=True, indent=2)
        else:
            fmts = ', '.join(list(self.keys))
            raise ConfigurationError(('Output format must be one of: '
                                      '{}'.format(fmts)))
