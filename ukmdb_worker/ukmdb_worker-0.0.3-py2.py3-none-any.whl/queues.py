#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0330,C0103

from __future__ import absolute_import
from kombu.common import Queue, Exchange
from ukmdb_worker import __version__
from ukmdb_settings import settings


def setup(app):
    app.conf.update(

        CELERY_TASK_SERIALIZER='json',
        CELERY_ACCEPT_CONTENT=['json',
                               'application/json'],  # Ignore other content
        CELERY_RESULT_SERIALIZER='json',
        CELERY_TASK_RESULT_EXPIRES=30,
        CELERY_ENABLE_UTC=True,
        CELERY_TIMEZONE=settings.CFG_TIMEZONE,
        # CELERY_RESULT_BACKEND='rpc://',
        CELERY_RESULT_BACKEND="amqp",
        CELERY_RESULT_PERSISTENT=True,
        CELERY_QUEUES=(
            Queue('ukmdb_monitoring01',
                  Exchange('ukmdb_all_in', type='topic'),),
            Queue('ukmdb_logst01',
                  Exchange('ukmdb_all_in', type='topic'),),
            Queue('ukmdb_id01',
                  Exchange('ukmdb_get_id'),
                  routing_key='ukmdb_id01'),
            Queue('ukmdb_itop01',
                  Exchange('ukmdb_all_in', type='topic'),),
            Queue('ukmdb_all_errors',
                  Exchange('ukmdb_error_in'),
                  routing_key='*.error'),
            Queue('ukmdb_graph01',
                  Exchange('ukmdb_all_in', type='topic'),),
        ),
        CELERY_ROUTES={},
        CELERY_CREATE_MISSING_QUEUES=False,
        CELERY_IGNORE_RESULT=True,
        CELERY_STORE_ERRORS_EVEN_IF_IGNORED=False,
        CELERY_DEFAULT_QUEUE='ukmdb_all_errors',
        CELERY_DEFAULT_EXCHANGE='ukmdb_error_in',
        CELERY_DEFAULT_ROUTING_KEY='ukmdb.warn',
    )
