class Condition(object):
    FAIR = None
    GOOD = None
    POOR = None
    UNSTABLE = None

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
        if name == 'FAIR' or name == '0':
            return getattr(Condition, 'FAIR')
        elif name == 'GOOD' or name == '1':
            return getattr(Condition, 'GOOD')
        elif name == 'POOR' or name == '2':
            return getattr(Condition, 'POOR')
        elif name == 'UNSTABLE' or name == '3':
            return getattr(Condition, 'UNSTABLE')
        raise ValueError(name)

    @classmethod
    def values(cls):
        return (Condition.FAIR, Condition.GOOD, Condition.POOR, Condition.UNSTABLE,)

Condition.FAIR = Condition('FAIR', 0)
Condition.GOOD = Condition('GOOD', 1)
Condition.POOR = Condition('POOR', 2)
Condition.UNSTABLE = Condition('UNSTABLE', 3)
