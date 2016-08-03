# coding: utf-8
from __future__ import absolute_import

from celery import Celery

from twitprof.models import connect_to_database


def create_celery_app():
    celery_app = Celery('twitprof.tasks', include=['twitprof.tasks.tasks'])
    celery_app.config_from_envvar('TWITPROF_CELERY_SETTINGS')
    connect_to_database(database_name='twitter')
    return celery_app


app = create_celery_app()
