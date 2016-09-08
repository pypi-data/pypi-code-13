from __future__ import absolute_import, unicode_literals
from icicle import FrozenDict
from namespaces import Namespace

class FrozenNamespace(FrozenDict):
  '''Immutable, hashable Namespace.'''

  RESERVED = frozenset(['_dict', '_hash'])

  def __init__(self, *args, **kwargs):
    self._hash = None
    super(self.__class__, self).__init__(*args, **kwargs)

  def __getattr__(self, name):
    '''Behaves similarly to collections.namedtuple#__getattr__.'''
    try:
      return self[name]
    except KeyError:
      raise AttributeError(
        "'{}' object has no attribute '{}'".format(type(self).__name__, name)
      )

  def __setattr__(self, name, value):
    if name not in FrozenNamespace.RESERVED:
      raise AttributeError(
        "'{}' object has no attribute '{}'".format(type(self).__name__, name)
      )
    super(self.__class__, self).__setattr__(name, value)

  def __repr__(self):
    '''Representation is a valid python expression for creating a FrozenNamespace
    (assuming contents also implement __repr__ as valid python expressions).'''
    items = ('{}={}'.format(k,repr(v)) for k,v in self.iteritems())
    return '{}({})'.format(type(self).__name__, ', '.join(items))

  def __eq__(self, other):
    return isinstance(other, type(self)) and super(self.__class__, self).__eq__(other)

  def __ne__(self, other):
    return not self == other

  def __hash__(self):
    '''Caches lazily-evaluated hash for performance.'''
    if self._hash is None:
      self._hash = hash(frozenset(self.items()))
    return self._hash

