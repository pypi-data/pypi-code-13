"""
The settings app can be used to store global and app specific settings used
by arpegio.
"""
from django.conf import settings as django_settings


class SettingsSite(object):
    """
    A SettingsSite object encapsulates an instance of the Django settings
    application. Settings are registered with the SettingsSite using the
    register() method.
    """

    def __init__(self):
        self._settings = {}

    def register_global(self):
        """Register the project settings."""
        arpegio_settings = getattr(django_settings, 'ARPEGIO_SETTINGS', {})
        arpegio_settings = self._lower_keys(arpegio_settings)
        self._settings = arpegio_settings

    def register(self, settings_dict):
        """Update the settings."""
        self._settings.update(settings_dict)
        self._settings = self._lower_keys(self._settings)

    def _lower_keys(self, in_object):
        if isinstance(in_object, dict):
            lower_dict = {}
            for key, item in in_object.items():
                lower_dict[key.lower()] = self._lower_keys(item)
            return lower_dict
        else:
            return in_object

    @property
    def settings(self):
        """Return the settings dictionary."""
        return self._settings


site = SettingsSite()  # pylint: disable=invalid-name
