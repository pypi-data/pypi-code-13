"""
App configuration for ``notifications`` app.
"""

# Register signal handlers, but avoid interacting with the database.
# See: https://docs.djangoproject.com/en/1.8/ref/applications/#django.apps.AppConfig.ready

from django.apps import AppConfig


class NotificationsAppConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        # Import signals to make sure they get loaded.
        import notifications.signals
