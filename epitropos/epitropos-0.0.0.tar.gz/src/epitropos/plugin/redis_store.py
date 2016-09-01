# -*- coding: utf-8 -*-
from epitropos.plugin import (
    storage_plugin,
    StoragePlugin
)
from malibu.util.log import LoggingDriver
from redis import StrictRedis

_LOG = LoggingDriver.find_logger()


@storage_plugin(
    name='redis'
)
class RedisStorage(StoragePlugin):

    @classmethod
    def requirements(cls):
        """ Requirements (from pip) for running this plugin.
        """

        return [
            'redis == 2.10.5',
        ]

    def __init__(self, **options):

        super(self.__class__, self).__init__(**options)

        attrs = [
            'host',
            'port',
            'secret',
            'database',
            'expire',
            'prefix',
        ]

        defaults = {
            'database': 0,
            'secret': None,
            'expire': 36000,
            'prefix': 'epitropos:',
        }

        for attr in attrs:
            if not hasattr(self, attr):
                if attr not in options and attr not in defaults:
                    raise AttributeError('No option "%s" given!' % (attr))
                elif attr in options:
                    setattr(self, attr, options[attr])
                elif attr in defaults:
                    setattr(self, attr, defaults[attr])
            else:
                continue

        _LOG.debug('Loaded Redis connection data: redis://%s@%s:%s/%s' % (
            self.secret,
            self.host,
            self.port,
            self.database))

    def connect(self, **kwargs):
        """ Connects to a Redis instance and passes any addition params from
            kwargs into the StrictRedis initializer.
        """

        args = {
            'host': self.host,
            'port': self.port,
            'db': int(self.database),
            'password': self.secret,
        }

        for k, v in kwargs.items():
            if k in args:
                _LOG.warning('Ignoring duplicate value %s with value %s' % (
                    k,
                    v
                ))
            else:
                args.update({k: v})

        self._client = StrictRedis(**args)
        try:
            if not self._client.ping():
                return False
            else:
                return True
        except:
            return False

    def ping(self):
        """ Pings the storage backend.
        """

        try:
            self._client.ping()
        except Exception as e:
            _LOG.warning(' ==> Exception while pinging backend: %s' % (str(e)))
            return False

        return True

    def insert(self, key, datamap):
        """ Inserts a hash of data into the Redis store.
        """

        key_name = self._key(key)

        try:
            self._client.hmset(key_name, datamap)
            self._client.expire(key_name, self.expire)
        except Exception as e:
            # Shit...
            _LOG.warning(' ==> Exception while inserting data: %s' % (str(e)))
            return False

        return True

    def remove(self, key, expire=False):
        """ Removes a key from the Redis store.
        """

        key_name = self._key(key)

        if self._client.exists(key_name):
            _LOG.debug('Deleting key: %s' % (key_name))
            res = self._client.delete(key_name)
            if res:
                return True
            else:
                return False
        else:
            return False

    def find(self, **searchopts):
        """ Searches for a certain value that is a part of a token.

            Easiest value to find is a key, which takes approximately O(n)
            to return from Redis (where `n` is hash size).

            Anything other than `key` which is specified in searchopts could
            be as quick as O(1) + O(n) (find + get, `n` is hash size) or as
            slow as O(n) + O(m) (find + get, `n` is collection size, m is hash
            size).
        """

        if 'key' in searchopts:
            key_name = self._key(searchopts.get('key'))
            if self._client.exists(key_name):
                return self._client.hgetall(key_name)
        else:
            for key in self._client.scan_iter(self._key('*')):
                data = self._client.hgetall(key)
                for k, v in searchopts.items():
                    if k not in data:
                        continue

                    if data[k] != str(v):
                        continue

                    data.update({
                        '__key': key,
                    })
                    return data

        return None

    def _key(self, name):
        """ Returns Redis key-format name.
            Consists of prefix + name.
        """

        return self.prefix + name
