
from django.apps import AppConfig

default_app_config = 'leonardo_diskcache.Config'


LEONARDO_APPS = ['leonardo_diskcache']


class Config(AppConfig):
    name = 'leonardo_diskcache'
    verbose_name = "leonardo-diskcache"
