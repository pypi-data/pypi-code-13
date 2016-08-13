from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


# DJANGO SETTINGS ##################################################################################
def get_setting(setting_name, default):
    """
    Obtains the setting based by name from a dictionary named
    `ICEKIT_NOTIFICATIONS` in Django settings. If none is found a default
    is used.

    :param setting_name: The setting name to look for.
    :param default: The default value if not setting provided.
    :return: The value in settings or if not present the default.
    """
    if hasattr(settings, 'ICEKIT_NOTIFICATIONS'):
        publishing_settings = getattr(settings, 'ICEKIT_NOTIFICATIONS')
        if not isinstance(publishing_settings, dict):
            raise ImproperlyConfigured('ICEKIT_NOTIFICATIONS setting must be a dictionary.')
        if setting_name in publishing_settings.keys():
            return publishing_settings[setting_name]
    return default

# DJANGO MODEL SETTINGS ############################################################################
def get_no_notifications_name():
    return get_setting('NO_NOTIFICATIONS_NAME', _('No notifications'))


def get_email_notifications_name():
    return get_setting('EMAIL_NOTIFICATIONS_NAME', _('Email only'))


def get_internal_notifications_name():
    return get_setting('INTERNAL_NOTIFICATIONS_NAME', _('Internal only'))


def get_all_notifications_name():
    return get_setting('ALL_NOTIFICATIONS_NAME', _('Email and internal'))


def get_notification_from_email():
    return get_setting('NOTIFICATION_FROM_EMAIL', 'no-reply@localhost')


def create_notification_settings_for_staff_only():
    return get_setting('STAFF_ONLY_NOTIFICATIONS', True)
