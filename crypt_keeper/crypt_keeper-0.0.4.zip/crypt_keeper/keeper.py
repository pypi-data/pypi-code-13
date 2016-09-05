import os
import pickle

class Keeper:

    def __init__(self, dbfile):
        self.dbfile = dbfile
        if os.path.exists(dbfile):
            binary = open(dbfile, 'rb').read()
            self._dict = pickle.loads(binary)
        else:
            self._dict = {}

    def __del__(self):
        fp = open(self.dbfile, 'wb')
        binary = pickle.dumps(self._dict)
        fp.write(binary)
        fp.close()

    def __getitem__(self, key):
        key = key.lower()
        return self._dict[key]

    def __setitem__(self, key, value):
        key = key.lower()
        self._dict[key] = value

    def __contains__(self, key):
        key = key.lower()
        return key in self._dict
