from __future__ import absolute_import, unicode_literals
import collections
from six import iteritems

class FrozenNamespace(collections.Mapping):
  '''Immutable, hashable dictionary whose items are also available via dot-notation.'''

  RESERVED = frozenset(['_dict', '_hash'])

  def __init__(self, *args, **kwargs):
    self._dict = dict(*args, **kwargs)
    self._hash = None

  def __getattr__(self, name):
    '''Look up item via dot-notation.'''
    if name not in self._dict:
      message = "'{}' object has no attribute '{}'"
      raise AttributeError(message.format(type(self).__name__, name))
    return self._dict[name]

  def __setattr__(self, name, value):
    '''Disable setting items via dot-notation to protect against accidental mutations.'''
    if name in FrozenNamespace.RESERVED:
      super(self.__class__, self).__setattr__(name, value)
    else:
      message = "'{}' object has no attribute '{}'"
      raise AttributeError(message.format(type(self).__name__, name))

  def __repr__(self):
    '''Representation is a valid python expression for creating a FrozenNamespace
    (assuming contents also implement __repr__ as valid python expressions).'''
    items = ('{}={}'.format(k,repr(v)) for k,v in sorted(iteritems(self)))
    return '{}({})'.format(type(self).__name__, ', '.join(items))

  def __hash__(self):
    '''Caches lazily-evaluated hash for performance.'''
    if self._hash is None:
      self._hash = hash(frozenset(iteritems(self)))
    return self._hash

  # dict pass-through
  ###################

  def __getitem__(self, name):
    return self._dict[name]

  def __iter__(self):
    return iter(self._dict)

  def __len__(self):
    return len(self._dict)

