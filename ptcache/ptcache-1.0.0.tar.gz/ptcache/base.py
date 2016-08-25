"""
Cache
    :copyright: (c) 2016 by beginman.
    :license: MIT, see LICENSE for more details.
"""

import logging
import redis
import json

from decimal import Decimal
from datetime import datetime, timedelta, date

try:
    import cPickle as pickle
except ImportError:
    import pickle


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton


def json_process(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        raise TypeError('%r is not JSON serializable' % obj)


class BaseCache(object):
    def __init__(self, timeout=None, pickle=pickle):
        self.timeout = timeout
        self.pickle = pickle

    def dumps(self, value, json_process=json_process):
        if self.pickle.__name__ in ('pickle', 'cPickle'):
            return self.pickle.dumps(value, self.pickle.HIGHEST_PROTOCOL)
        elif self.pickle.__name__ == 'json':
            return self.pickle.dumps(value, ensure_ascii=False,
                                     default=json_process)
        else:
            raise TypeError('Only support pickle and json.')

    def loads(self, val):
        return self.pickle.loads(val)

    def get(self, key):
        return None

    def get_many(self, *keys):
        return map(self.get, keys)

    def get_dict(self, *keys):
        return dict(zip(keys, self.get_many(*keys)))

    def set(self, key, value, timeout=None):
        pass

    def delete(self, key):
        pass

    def clear(self):
        pass

    def exists(self, key):
        pass

    def ttl(self, key):
        pass


@singleton
class SimpleCache(BaseCache):
    def __init__(self, timeout=300, threshold=1000, pickle=pickle):
        BaseCache.__init__(self, timeout, pickle)
        self._cache = dict()
        self._threshold = threshold

    def _prune(self):
        if len(self._cache) >= self._threshold:
            num = len(self._cache) - self._threshold + 1
            for key, value in sorted(self._cache.items(), key=lambda x:x[1][0])[:num]:
                self._cache.pop(key, None)

    def count(self):
        return len(self._cache)

    def get(self, key):
        expires, value = self._cache.get(key, (None, None))
        if expires is not None:
            if expires > datetime.now():
                return self.loads(value)
            else:
                self.delete(key)

        elif value is not None:
            return self.loads(value)
        return None

    def set(self, key, value, timeout=None):
        self._prune()

        value = self.dumps(value)
        timeout = self.timeout if timeout is None else None
        if timeout is None:
            self._cache[key] = (None, value)
        else:
            if isinstance(timeout, int):
                timeout = timedelta(seconds=timeout)
            self._cache[key] = (datetime.now() + timeout, value)
        return value

    def delete(self, key):
        self._cache.pop(key, None)

    def clear(self):
        for key, (expires, _) in self._cache.iteritems():
            if expires < datetime.now():
                self._cache.pop(key, None)

    def exists(self, key):
        return self.ttl(key) != -2

    def ttl(self, key):
        expires, value = self._cache.get(key, (None, None))
        if expires is not None:
            if expires > datetime.now():
                return (expires - datetime.now()).seconds
            else:
                self.delete(key)
        return -2


@singleton
class RedisCache(BaseCache):
    """ redis cache
    """
    def __init__(self, **kwargs):
        BaseCache.__init__(self, pickle=json)
        self._redis_pool = redis.ConnectionPool(**kwargs)
        self._redis_client = redis.StrictRedis(connection_pool=self._redis_pool)

    def get(self, key):
        try:
            value = self._redis_client.get(key)
            if value is not None:
                return self.loads(value)
        except Exception as ex:
            logging.warning(ex.message, exc_info=ex)

    def set(self, key, value, timeout=None):
        try:
            if timeout is not None:
                self._redis_client.setex(key, timeout, self.dumps(value))
            else:
                self._redis_client.set(key, self.dumps(value))
            return value
        except Exception as ex:
            logging.warning(ex.message, exc_info=ex)

    def delete(self, key):
        self._redis_client.delete(key)

    def exists(self, key):
        return self._redis_client.exists(key)

    def ttl(self, key):
        return self._redis_client.ttl(key)

