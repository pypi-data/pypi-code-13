import collections
import time


class TimedCache(collections.MutableMapping):
    '''A time-based cache that acts like a dictionary. Once a value's time
       has expired, it no longer appears to be in the dictionary and will
       be evicted.

       # create a new cache
       cache = new TimedCache(ttl=30)

       # add a value to it
       cache['key'] = value

       # retrieve items from it
       cache['key']
       cache.get('key')
       # value

       # wait 30 seconds

       cache.get('key')
       # None

       cache['key']
       # raises KeyError
    '''
    def __init__(self, ttl=86400):
        self.ttl = ttl
        self._data = {}

    def __getitem__(self, key):
        if key not in self._data:
            raise KeyError()
        item = self._data[key]
        if (time.time() - item[0]) < self.ttl:
            return item[1]
        else:
            del self._data[key]
            raise KeyError()

    def __setitem__(self, key, value):
        self._data[key] = (time.time(), value)

    def __delitem__(self, key):
        if key not in self._data:
            raise KeyError
        item = self._data[key]
        del self._data[key]
        if (time.time() - item[0]) >= self.ttl:
            raise KeyError()

    def __contains__(self, key):
        if key not in self._data:
            return False
        item = self._data[key]
        if (time.time() - item[0]) < self.ttl:
            return True
        else:
            del self._data[key]
            return False

    def __len__(self):
        length = 0
        now = time.time()
        keys_to_delete = []
        for key, value in self._data.items():
            if (now - value[0]) < self.ttl:
                length += 1
            else:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self._data[key]

        return length

    def __iter__(self):
        keys_to_delete = []
        for key, value in self._data.items():
            if (time.time() - value[0]) < self.ttl:
                yield key
            else:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del self._data[key]
