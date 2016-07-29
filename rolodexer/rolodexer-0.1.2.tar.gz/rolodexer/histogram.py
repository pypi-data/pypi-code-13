#!/usr/bin/env python
from __future__ import print_function

from collections import defaultdict, namedtuple
from operator import add
from math import floor

class AutoInc(object):
    # ''' Get a uniquely auto-incremented integer value '''
    __slots__ = ('v',)
    
    def __init__(self, value=0):
        self.v = int(value)
    
    def __call__(self):
        self.v += 1
        return self.v
    
    def add(self, value):
        self.v += int(value)
        return self.v
    
    def __int__(self):
        return self.v
    
    def __float__(self):
        return float(self.v)
    
    def __long__(self):
        return long(self.v)
    
    def __repr__(self):
        return str(self.v)
    
    def __str__(self):
        return str(self.v)

class Histogram(defaultdict):
    
    @staticmethod
    def lexcmp(k0, k1):
        """ Hacky comparator to privilege string length """
        return cmp(len(k1), len(k0)) or cmp(k0, k1)
    
    @staticmethod
    def autoinc():
        return AutoInc()
    
    def __init__(self, *args, **kwargs):
        for arg in args:
            argclsname = arg.__class__.__name__
            if argclsname.startswith('FrozenHistogram'):
                # reconstitute FrozenHistogram
                kwargs.update(arg._asdict())
            elif (argclsname.startswith('Histogram') or
                  argclsname.startswith('defaultdict') or
                  argclsname.startswith('dict')):
                # copy-construct
                kwargs.update(dict(arg))
            else:
                # normal arg: column name
                kwargs.update({ str(arg): AutoInc() })
        super(Histogram, self).__init__(AutoInc, *tuple(), **kwargs)
    
    def prettyprint(self, **kwargs):
        from pprint import pformat
        return "%s(%s,\n%s)" % (
            self.__class__.__name__,
            AutoInc.__name__,
            pformat(dict(self), **kwargs))
    
    def __repr__(self):
        return self.prettyprint()
    
    def __str__(self):
        longest_key = sorted(self.iterkeys(),
                             cmp=Histogram.lexcmp,
                             reverse=False)[0]
        return self.prettyprint(depth=10,
                                width=len(longest_key))
    
    def inc(self, idx):
        return self[str(idx)]()
    
    def add(self, idx, value):
        return self[str(idx)].add(value)
    
    def val(self, idx):
        return int(self[idx])
    
    def keyset_hash(self):
        return hex(abs(hash(self.iterkeys())))
    
    def frozentype(self, rename=True):
        return namedtuple('FrozenHistogram_%s' % self.keyset_hash(),
            tuple(self.iterkeys()), rename=rename)
    
    def freeze(self):
        return self.frozentype()(**self)
    
    def normalize(self):
        ceil = float(sum(int(v) for v in self.itervalues()))
        return self.frozentype()(**dict(
            (ituple[0], float(ituple[1]) / ceil) for ituple in self.iteritems()
        ))
    
    def max(self):
        """ Maximum value """
        return max(*(int(v) for v in self.values()))
    
    def min(self):
        """ Minimum value """
        return min(*(int(v) for v in self.values()))
    
    def sum(self):
        return reduce(add, (int(v) for v in self.itervalues()))
    
    def average(self):
        """ Histogram mean/average (float) """
        return float(self.sum()) / float(len(self))
    
    def avg(self):
        """ Histogram mean/average (integer) """
        return int(floor(self.average()))
    
    def range(self):
        """ Histogram numerical range (integer) """
        return self.max() - self.min()
    
    def valuelist(self):
        return sorted(int(v) for v in self.itervalues())
    
    def median(self):
        """ Median histogram value (integer, or int/2) """
        vals = self.valuelist()
        idx = len(vals) / 2
        if len(vals) % 2:
            return vals[idx+1]
        return float(vals[idx] + vals[idx+1]) / 2.0
    
    def keys_for_value(self, value):
        """ List of keys with the given integer value """
        return map(lambda pair: pair[0],
            filter(lambda pair: int(pair[1]) == int(value),
            self.iteritems()))
    
    def valueset(self):
        return set(self.valuelist())

if __name__ == '__main__':
    # Hh = Histogram('color', 'phone', 'zip', 'firstname', 'lastname')
    Hh = Histogram('color', 'phone', 'zip', firstname=10, lastname=10)
    Hp = Histogram(firstname=0, lastname=0)
    
    Hh['color']()
    Hh['color']()
    Hh['color']()
    Hh['color']()
    Hh['color']()
    Hh['color']()
    
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    Hh['phone']()
    
    Hh['zip']()
    Hh['zip']()
    Hh['zip']()
    Hh['zip']()
    
    print(Hh)
    print(Hh.freeze()._asdict())
    print(Hh.normalize())
    print('')
    
    # print("MAX Hh: %s" % max(*(int(v) for v in Hh.values())))
    print("MIN Hh: %s" % Hh.min())
    print("MAX Hh: %s" % Hh.max())
    print("SUM Hh: %s" % Hh.sum())
    print("AVG Hh: %s" % Hh.avg())
    print("RANGE Hh: %s" % Hh.range())
    print("MEDIAN Hh: %s" % Hh.median())
    print("KEYS IN Hh FOR 19: %s" % Hh.keys_for_value(19))
    print("KEYS IN Hh FOR 777: %s" % Hh.keys_for_value(777))
    print("KEYS IN Hh FOR 0: %s" % Hh.keys_for_value(0))
    print('')
    
    hh = Histogram(Hh, 'iheard', 'youlike', yo=10, dogg=100)
    
    print(hh)
    print(hh.freeze()._asdict())
    print(hh.normalize())
    print('')
    
    print("MIN hh: %s" % hh.min())
    print("MAX hh: %s" % hh.max())
    print("SUM hh: %s" % hh.sum())
    print("AVG hh: %s" % hh.avg())
    print("RANGE hh: %s" % hh.range())
    print("MEDIAN hh: %s" % hh.median())
    print("KEYS IN hh FOR 19: %s" % hh.keys_for_value(19))
    print("KEYS IN hh FOR 777: %s" % hh.keys_for_value(777))
    print("KEYS IN hh FOR 0: %s" % hh.keys_for_value(0))
    print('')
    
    Hp.inc('color')
    Hp.inc('color')
    Hp.inc('color')
    Hp.inc('color')
    Hp.inc('color')
    Hp.inc('color')
    
    Hp.inc('zip')
    Hp.inc('zip')
    
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    Hp.inc('phone')
    
    print(Hp)
    
    print(Hp.freeze()._asdict())
    print(Hp.normalize())
    
    print("MAX Hp: %s" % Hp.max())
