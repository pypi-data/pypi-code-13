#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0330,C0103
"""UKMDB Worker.

Usage: ukm_checkmk [--help] [--debug ...]

Options:
  -d --debug               Show debug information (maybe multiple).

  ukm_checkmk (-h | --help)
  ukm_checkmk --version

"""

from __future__ import absolute_import
import logging
from pprint import pformat
from celery import Celery
from docopt import docopt
from ukmdb_worker.base import set_debug_level
from ukmdb_worker import __version__
from ukmdb_worker import queues
from ukmdb_settings import settings


ukmdb_log = logging.getLogger("ukmdb")


app = Celery('worker',
             broker=settings.AMQP_BROKER_URL,
             )

queues.setup(app)


@app.task(serializer='json',
          name='worker.add_object',
          queue='ukmdb_monitoring01',
          exchange='ukmdb_all_in',
          routing_key='#',
          bind=True
          )
def add_object(self, msg):
    ukmdb_log.debug("-------> self.request: '%s'", pformat(self.request))
    ukmdb_log.debug("check_mk # add_object: '%s'", str(msg))


def main():
    arguments = docopt(__doc__, options_first=True, version=__version__)
    set_debug_level(ukmdb_log, arguments)

    ukmdb_log.debug(u'program start')
    app.start()

    exit("See 'ukm_checkmk --help'.")
