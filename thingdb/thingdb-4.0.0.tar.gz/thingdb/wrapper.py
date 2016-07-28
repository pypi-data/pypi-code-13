try:
    from UserDict import DictMixin
except ImportError:
    from collections import MutableMapping as DictMixin

from . import encoder

class Wrapper(DictMixin):
    """Main wrapper for thingdb"""
    def __init__(self, dict):
        self.dict = dict
        self.cache={}
    def keys(self):
        return self.dict.keys()
    def has_key(self, key):
        return key in self.dict
    def __getitem__(self, key):
        if key not in self.cache.keys():
            self.cache[key] = encoder.depickle(self.dict[key])
        return self.cache[key]
    def __setitem__(self, key, value):
        self.cache[key] = value
    def __delitem__(self, key):
        try:
            del self.dict[key]
        except KeyError:
            del self.cache[key]
    def __contains__(self, key):
        return key in self.dict
    def __len__(self):
        return len(self.dict)
    def __iter__(self):
        for k in self.dict.keys():
            if k in self.cache.keys:
                yield k, self.cache[k]
            else:
                yield k, encoder.depickle(self.dict[k])