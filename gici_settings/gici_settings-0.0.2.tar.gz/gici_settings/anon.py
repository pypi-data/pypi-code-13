class AnonObject(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        from pprint import PrettyPrinter
        return PrettyPrinter().pformat(self.__dict__)

    def pop(self, key):
        self.__dict__.pop(key)

    def __repr__(self):
        return str(self)