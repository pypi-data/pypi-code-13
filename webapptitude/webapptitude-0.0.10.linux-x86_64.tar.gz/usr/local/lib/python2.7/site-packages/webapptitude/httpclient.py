import httplib2
import pickle
from google.appengine.api import memcache

import logging


class MemcacheProxy(object):

    CHUNK_SIZE = (1000000 - 1)

    def __init__(self, namespace=None, lifetime=None):
        self.namespace = (namespace or 'ns')
        self.lifetime = lifetime

    @classmethod
    def serialize(cls, value):
        value = pickle.dumps(value, 2)
        for i in xrange(0, len(value), cls.CHUNK_SIZE):
            yield (i // cls.CHUNK_SIZE), value[i:(i + cls.CHUNK_SIZE)]

    @classmethod
    def deserialize(cls, chunks):
        assert isinstance(chunks, list)
        return pickle.loads(''.join(chunks))

    def get(self, key, **kwargs):
        kwargs['namespace'] = kwargs.get('namespace', self.namespace)

        chunklist = memcache.get(key, **kwargs)  # retrieve the list of parts
        logging.debug("Cache retrieve %r: %r" % (key, chunklist))

        if isinstance(chunklist, list):
            # Retrieve each part
            chunklist = [memcache.get(i, **kwargs) for i in chunklist]
            # Compile the result
            return self.deserialize(chunklist)

        return chunklist

    def set(self, key, value, **kwargs):
        kwargs['namespace'] = kwargs.get('namespace', self.namespace)
        kwargs['time'] = kwargs.get('time', self.lifetime)
        chunklist = []
        for ident, chunk in self.serialize(value):
            chunk_key = ('%s$%d' % (key, ident))
            chunklist.append(chunk_key)
            logging.debug("Cache write %r, (%d)" % (chunk_key, len(chunk)))
            memcache.set(chunk_key, chunk, **kwargs)

        logging.debug("Cache write %r, (%d)" % (key, len(chunklist)))
        return memcache.set(key, chunklist, **kwargs)

    def delete(self, key, **kwargs):
        kwargs['namespace'] = kwargs.get('namespace', self.namespace)
        return memcache.delete(key, seconds=0, **kwargs)

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        return self.set(name, value)

    def __delitem__(self, name):
        return self.delete(name)


class HTTPCache(MemcacheProxy):

    def __init__(self, namespace=None, lifetime=None):
        if lifetime is None:
            lifetime = 600  # default 10 minutes
        namespace = 'http#%s' % (namespace or "__default__")
        super(HTTPCache, self).__init__(namespace=namespace,
                                        lifetime=lifetime)


class HTTP(httplib2.Http):

    def __init__(self, timeout=60, cache=None, namespace=None, lifetime=None):
        cache = cache or HTTPCache(namespace=namespace, lifetime=lifetime)
        super(HTTP, self).__init__(timeout=timeout, cache=cache)
