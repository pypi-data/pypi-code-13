#--------------------------------------------------------------------
# Xenum: A simple alternative to Python 3 enums, offering easy
#        conversion to and from strings.
#
# Author: Lain Supe (lainproliant)
# Date: Wednesday, August 31st 2016
#
# Released under a 3-clause BSD license, see LICENSE for more info.
#--------------------------------------------------------------------
import inspect

#--------------------------------------------------------------------
class EqualityMixin:
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

#--------------------------------------------------------------------
class Xenum(EqualityMixin):
    """
    An enumeration instance.
    """
    def __init__(self, typename, name, value):
        self.typename = typename
        self.name = name
        self.value = value
    
    def value(self):
        return self.value

    def __str__(self):
        return '%s.%s' % (self.typename, self.name)

#--------------------------------------------------------------------
def xenum(clazz):
    """
    Converts a basic class' attributes into Xenum instances.
    Use this annotation on classes you would like to treat as
    enumerations.
    """
    class_attrs = inspect.getmembers(clazz, lambda attr: not inspect.isroutine(attr))
    class_attrs = [a[0] for a in class_attrs if not a[0].startswith('__') and not a[0].endswith('__')]

    xenum_map = {}
    for attr in class_attrs:
        xenum_instance = Xenum(clazz.__name__, attr, getattr(clazz, attr))
        xenum_map['%s.%s' % (clazz.__name__, attr)] = xenum_instance
        setattr(clazz, attr, xenum_instance)

    def by_name(name):
        if not name in xenum_map:
            raise ValueError('Enum "%s" has no member "%s"' % (clazz.__name__, name))
        return xenum_map[name]

    setattr(clazz, 'by_name', by_name)

    return clazz

