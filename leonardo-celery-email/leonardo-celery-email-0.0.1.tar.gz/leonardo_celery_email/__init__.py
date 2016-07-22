
from django.apps import AppConfig

default_app_config = 'leonardo_celery_email.Config'


LEONARDO_APPS = ['leonardo_celery_email', 'djcelery_email']


class Config(AppConfig):
    name = 'leonardo_celery_email'
    verbose_name = "leonardo-celery-email"
