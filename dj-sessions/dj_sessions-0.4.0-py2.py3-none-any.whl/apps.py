from django.apps import AppConfig


class DJSessionsConfig(AppConfig):
    name = 'djsessions'
    verbose_name = 'djsessions'

    def ready(self):
        from .signals import user_logged_in  # noqa
        from .signals import user_logged_out  # noqa
        from .signals import post_delete  # noqa
