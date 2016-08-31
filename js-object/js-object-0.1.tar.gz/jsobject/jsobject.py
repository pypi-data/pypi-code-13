import json as json_parser
import doctest


class JSObject:
    """Allow to use json as an Python object with attributes

    >>> jso = JSObject({'attr1': {'attr2': 'val1'}, 'attr3': ['val2', {'attr4': 'val3'}]})
    >>> jso.attr1.attr2
    'val1'
    >>> jso.attr3[1].attr4
    'val3'
    >>> jso.new_attr = 'new val'
    >>> jso.new_attr
    'new val'
    >>> jso.no_attr
    {}
    >>> jso.no_attr = 'no val'
    >>> jso.no_attr
    'no val'
    >>> jso.attr1
    {'attr2': 'val1'}
    >>> jso.attr3
    ['val2', {'attr4': 'val3'}]

    """

    def __init__(self, json):
        if isinstance(json, str):
            json = json_parser.loads(json)
        self.json = json

    def __getattr__(self, attr):

        if attr in dir(list) + dir(dict):
            return getattr(self.json, attr)

        try:
            val = self.json[attr]
        except KeyError or IndexError or TypeError:
            self.json[attr] = {}
            return JSObject(self.json[attr])

        if isinstance(val, (list, dict)):
            return JSObject(val)

        if isinstance(val, (str, int, float)):
            return val

    def __setattr__(self, key, value):
        if key in dir(JSObject) + ['json']:
            super().__setattr__(key, value)
        else:
            self.json.update({key: value})

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __str__(self):
        return str(self.json)

    def __repr__(self):
        return str(self.json)


if __name__ == '__main__':
    doctest.testmod()
