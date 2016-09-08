"""define some wrapper for memcache client `pymemcache`
"""

import logging
from tingyun.armoury.ammunition.memcache_tracker import wrap_memcache_trace


console = logging.getLogger(__name__)
methods = ['add', 'append', 'cas', 'decr', 'delete', 'delete_many', 'delete_multi', 'flush_all', 'get',
           'get_many', 'get_multi', 'gets', 'gets_many', 'incr', 'prepend', 'replace', 'set', 'set_many', 'set_multi',
           'stats']


def detect_base_client(module):
    """
    :param module:
    :return:
    """
    for m in methods:
        if hasattr(module.Client, m):
            wrap_memcache_trace(module, 'Client.%s' % m, m)
            console.debug("Wrap the base client method %s", m)


def detect_pooled_client(module):
    """for Pooled client
    :param module:
    :return:
    """
    if not hasattr(module, "PooledClient"):
        console.info("Pooled Client not in this version.")
        return

    for m in methods:
        if hasattr(module.PooledClient, m):
            wrap_memcache_trace(module, 'PooledClient.%s' % m, m)
            console.debug("Wrap the base pooled client method %s", m)


def detect_has_client(module):
    """this is a client for communicating with a cluster of memcached servers
    :param module:
    :return:
    """
    for m in methods:
        if hasattr(module.HashClient, m):
            wrap_memcache_trace(module, 'HashClient.%s' % m, m)
            console.debug("Wrap the hash client method %s", m)
