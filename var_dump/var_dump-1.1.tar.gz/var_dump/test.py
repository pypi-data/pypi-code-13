__author__ = 'sha256'

from var_dump import var_dump
from datetime import datetime
from decimal import Decimal


basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
fruit = set(basket)

dt = open('../setup.cfg')

var_dump(dt)

var_dump(basket)


class Base(object):

    def __init__(self):
        self.baseProp = (33, 44)
        self.fl = 44.33

class Bar(object):

    def __init__(self):
        self.barProp = "I'm from Bar class"
        self.boo = True


class Foo(Base):

    def __init__(self):
        super(Foo, self).__init__()
        self.someList = ['foo', 'goo']
        self.someTuple = (33, (23, 44), 55)
        self.anOb = Bar()
        self.no = None

foo = Foo()
var_dump(foo)