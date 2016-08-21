"""
dici - dicts made easy
"""

class dici(dict):

    def __init__(self, **fields):
        for (key, value) in fields.items():
            self.__setitem__(key, value)

    def __delitem__(self, key):
        if '.' in key:
            obj = self
            prev = None
            for part in key.split('.'):
                prev = obj
                obj = obj[part]
            del prev[part]
        else: dict.__delitem__(self, key)

    __delattr__ = __delitem__

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = dici(**value)
            dict.__setitem__(self, key, value)

        else:
            dict.__setitem__(self, key, value)

    def __getitem__(self, key):
        if '.' in key:
            obj = self

            for part in key.split('.'):
                if obj is None:
                    return None

                obj = obj[part]

            return obj
        else:
            return dict.__getitem__(self, key)

    def __getattr__(self, key):
        if key in self.__dict__:
            return dict.__getattr__(self, key)
        else:
            return self.__getitem__(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __contains__(self, item):
        try:
            self.__getitem__(item)
            return True
        except:
            return False

    def __iter__(self):
        return dict.__iter__(self)

    def set(self, key, value):
        """
        set the key by making sure to construct a path with separate
        dictionaries for each element in the key with a `.` separating
        the names in the key.
        """
        if '.' in key:
            obj = self
            for part in key.split('.')[:-1]:

                if part not in obj:
                    obj[part] = dici()

                obj = obj[part]

            exec('self.%s="%s"' % (key, value))

        else:
            dict.__setitem__(self, key, value)
