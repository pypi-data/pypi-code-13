# coding=utf-8

import os
import importlib

from monstro.core.exceptions import ImproperlyConfigured
from monstro.core.constants import SETTINGS_ENVIRONMENT_VARIABLE
from monstro.utils.imports import import_object
from monstro.modules import ModulesRegistry

from .schema import SettingsSchema


def _import_settings_class():
    try:
        settings_class = import_object(
            os.environ[SETTINGS_ENVIRONMENT_VARIABLE]
        )
    except KeyError:
        raise ImproperlyConfigured(
            'You must either define the environment variable {}'.format(
                SETTINGS_ENVIRONMENT_VARIABLE
            )
        )

    data = {key: getattr(settings_class, key) for key in dir(settings_class)}

    print(data['debug'])

    try:
        SettingsSchema.validate(data)
    except SettingsSchema.ValidationError as e:
        raise ImproperlyConfigured(
            'Wrong settings. {}'.format(
                ' '.join('{}: {}.'.format(*pair) for pair in e.error.items())
            )
        )

    return settings_class


settings = _import_settings_class()
modules = ModulesRegistry(settings.modules)
