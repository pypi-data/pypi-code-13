from django.apps.config import AppConfig
from django.conf import settings


class I18nKitAppConfig(AppConfig):
    name = 'i18nkit'

    def ready(self):
        if getattr(settings, 'I18NKIT_POISON', False):  # pragma: no cover
            from .poison import enable
            enable()
