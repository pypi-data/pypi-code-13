#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0330,C0103,W0612
"""UKMDB check_mk adapter.

Usage: ukm_checkmk_sb_get_all [--help] [--debug ...]

Options:
  -d --debug               Show debug information (maybe multiple).

  ukm_checkmk_sb_get_all (-h | --help)
  ukm_checkmk_sb_get_all --version

"""

from __future__ import absolute_import
import logging
import pprint
from docopt import docopt
from ukmdb_worker.base import set_debug_level
from ukmdb_checkmk import host as wato_host
from ukmdb_checkmk import cmd
from ukmdb_checkmk import __version__
from ukmdb_settings import settings_wato


ukmdb_log = logging.getLogger("ukmdb")


def main():
    arguments = docopt(__doc__, options_first=True, version=__version__)
    set_debug_level(ukmdb_log, arguments)

    ukmdb_log.debug(u'program start')

    CONTEXT = {'wato_url': settings_wato.CFG_WATO_URL,
               'username': settings_wato.CFG_WATO_USERNAME,
               'password': settings_wato.CFG_WATO_PASSWORD,
               }

    c_mk_host01 = wato_host.CheckMkHost(context=CONTEXT,
                                        folder='Tests',
                                        hostname='Hase')

    ukmdb_log.info('starting .. 100x getter ..')
    for i in range(100):
        dummy = c_mk_host01.attributes['ipaddress']  # noqa: F841

    ukmdb_log.info('IP address after 100 get requests')
    ukmdb_log.info('ip address: %s', c_mk_host01.attributes['ipaddress'])

    # pprint.pprint(c_mk_host01.attributes['alias'])
    # pprint.pprint(c_mk_host01.alias)
    ukmdb_log.info('host alias 1: %s', c_mk_host01.attributes['alias'])
    ukmdb_log.info('host alias 2: %s', c_mk_host01.alias)
    #
    # c_mk_host01.alias += '_dd'
    # c_mk_host01.commit()

    ddd = cmd.GetAllHosts(settings_wato.CFG_WATO_URL,
                          settings_wato.CFG_WATO_USERNAME,
                          settings_wato.CFG_WATO_PASSWORD)
    ret_ddd = ddd.send_request()

    pprint.pprint(ret_ddd)

    ukmdb_log.debug(u'program stop')
    exit(0)
