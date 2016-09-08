"""define some wrapper for memcache client `python-binary-memcache`
"""

import logging
from tingyun.armoury.ammunition.memcache_tracker import wrap_memcache_trace

console = logging.getLogger(__name__)
methods = ['add', 'cas', 'decr', 'delete', 'delete_multi', 'delete_multi', 'get',
           'get_multi', 'gets', 'incr', 'replace', 'set', 'set_multi',
           'stats']


def detect_client(module):
    """
    :param module:
    :return:
    """
    for m in methods:
        if hasattr(module.Client, m):
            wrap_memcache_trace(module, 'Client.%s' % m, m)
            console.debug("Wrap the base client method %s", m)
