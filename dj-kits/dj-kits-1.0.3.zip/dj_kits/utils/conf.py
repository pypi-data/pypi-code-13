# -*- coding: utf-8 -*-
import inspect
import os
from django.core.exceptions import ImproperlyConfigured

_missing = object()


def _globals():
    frame = inspect.currentframe()
    try:
        caller = frame.f_back.f_back
        return caller.f_globals
    finally:
        del frame


def _get_project_name():
    module_name = os.environ.get('DJANGO_SETTINGS_MODULE', '')
    return module_name.split('.')[0].upper()


def _convert_variable(val, klass):
    if klass is None or isinstance(val, klass):
        return val
    elif klass is bool:
        return val in ['1', 'true', 'True', True]
    elif klass in (list, tuple):
        return klass(val.split(','))
    return klass(val)


class Config(object):

    def __init__(self, prefix=None):
        self.prefix = prefix or _get_project_name()

    def get(self, var_name, default=_missing, klass=None):
        prefix = self.prefix

        if var_name in _globals():
            val = _globals()[var_name]
        else:
            keys = [prefix + '_' + var_name, var_name]
            val = next((os.environ[key] for key in keys if key in os.environ), default)

        if val is not _missing:
            try:
                return _convert_variable(val, klass)
            except ValueError:
                error_msg = "%s environ variable requires %s type" % (" or ".join(keys), klass.__name__)
                raise ImproperlyConfigured(error_msg)
        else:
            error_msg = "Set the %s environ variable" % " or ".join(keys)
            raise ImproperlyConfigured(error_msg)


config = Config()
