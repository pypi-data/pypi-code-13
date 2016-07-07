from __future__ import unicode_literals, division, absolute_import
from builtins import *  # pylint: disable=unused-import, redefined-builtin

import logging

from flexget import plugin
from flexget.event import event

log = logging.getLogger('nzbget')


class OutputNzbget(object):
    """
    Example::

      nzbget:
        url: http://nzbget:12345@localhost:6789/xmlrpc
        category: movies
        priority: 0
        top: False
    """

    schema = {
        'type': 'object',
        'properties': {
            'url': {'type': 'string'},
            'category': {'type': 'string', 'default': ''},
            'priority': {'type': 'integer', 'default': 0},
            'top': {'type': 'boolean', 'default': False}
        },
        'required': ['url'],
        'additionalProperties': False
    }

    def on_task_output(self, task, config):
        from xmlrpc.client import ServerProxy

        params = dict(config)

        server = ServerProxy(params["url"])

        for entry in task.accepted:
            if task.options.test:
                log.info('Would add into nzbget: %s' % entry['title'])
                continue

            # allow overriding the category
            if 'category' in entry:
                params['category'] = entry['category']

            try:
                server.appendurl(entry["title"] + '.nzb',
                                 params["category"],
                                 params["priority"],
                                 params["top"],
                                 entry["url"])
                log.info("Added `%s` to nzbget" % entry["title"])
            except:
                log.critical("rpc call to nzbget failed")
                entry.fail("could not call appendurl via RPC")


@event('plugin.register')
def register_plugin():
    plugin.register(OutputNzbget, 'nzbget', api_ver=2)
