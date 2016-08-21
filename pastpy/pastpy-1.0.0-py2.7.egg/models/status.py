class Status(object):
    OK = None
    LOST = None
    ON_LOAN = None

    def __init__(self, name, value):
        object.__init__(self)
        self.__name = name
        self.__value = value

    def __int__(self):
        return self.__value

    def __repr__(self):
        return self.__name

    def __str__(self):
        return self.__name

    @classmethod
    def value_of(cls, name):
        if name == 'OK' or name == '0':
            return getattr(Status, 'OK')
        elif name == 'LOST' or name == '1':
            return getattr(Status, 'LOST')
        elif name == 'ON_LOAN' or name == '2':
            return getattr(Status, 'ON_LOAN')
        raise ValueError(name)

    @classmethod
    def values(cls):
        return (Status.OK, Status.LOST, Status.ON_LOAN,)

Status.OK = Status('OK', 0)
Status.LOST = Status('LOST', 1)
Status.ON_LOAN = Status('ON_LOAN', 2)
