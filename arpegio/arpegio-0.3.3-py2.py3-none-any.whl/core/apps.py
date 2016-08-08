from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

from .settings import site


class CoreConfig(AppConfig):
    name = 'arpegio.core'
    label = 'arpegio-core'


class CoreSettingsConfig(CoreConfig):

    def ready(self):
        super(CoreConfig, self).ready()
        autodiscover_modules('settings')
        site.register_global()
