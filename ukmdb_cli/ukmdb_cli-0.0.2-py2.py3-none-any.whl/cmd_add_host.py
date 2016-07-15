#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=
"""usage: ukm_cli [--debug ...] add_host [--help] <fqdn>

Arguments:
  fqdn                fqdn of the host

Options:
  -h --help                Show this add_host command screen.
  -d --debug               Show debug information.
"""

from time import sleep
import logging
import uuid
from schema import Schema, Optional, And, Use
# from ukmdb_worker import worker
# from ukmdb_graph import worker
from ukmdb_audit import worker

ukmdb_log = logging.getLogger("ukmdb")

SCHEMA = Schema({
    'add_host': bool,
    '<fqdn>': Use(str),
    Optional('--help'): bool,
    Optional('--debug'): And(Use(int), lambda n: n in (0, 1, 2, 3)),
})


def cmd(args):
    ukmdb_log.debug("starting command 'add_host'")
    print("#############  add_host  #############")

    enterprise_number = '1.3.6.1.4.1.7052.'
    app_domain = 'kvm@ikom'
    app_type = 'vhost'
    app_name = 'kvm@adm000-kvm16f'
    app_id = '040_ldap001c'

    oid_cat = enterprise_number + '%' + \
        app_domain + '%' + app_type + '%' + \
        app_name + '%' + app_id

    object_dict = {
        'type': 'host',
        'uuid': str(uuid.uuid5(uuid.NAMESPACE_OID, oid_cat)),
        'comment': 'Alien vs. Predator',
    }
    # worker.add_object.delay(object_dict)
    for i in range(1000):
        print('.', end="", flush=True)
        worker.add_object.apply_async((object_dict,),
                                      exchange='ukmdb_all_in',
                                      # routing_key='ddd8',
                                      # reply_to='ddd9',
                                      # reply_to='ukmdb_all_errors',
                                      expires=60)
        sleep(0.05)
    # while not res.ready():
    #     sleep(0.5)
    # res_output = res.get()
    # print("output: '%s'" % str(res_output))
    # import pdb
    # pdb.set_trace()
    # print(res)
    # res.forget()
    # worker.ukmdb_error.delay('Tote tragen keine Karos')
    print(args)
    ukmdb_log.debug(str(args))
    ukmdb_log.debug("command 'add_host' stopped")
