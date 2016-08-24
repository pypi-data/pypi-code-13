import collections

class FrozenDict(collections.Mapping):

  def __init__(self, *args, **kwargs):
    self._dict = dict(*args, **kwargs)
    self._hash = None

  def __getitem__(self, key):
    return self._dict[key]

  def __iter__(self):
    return iter(self._dict)

  def __len__(self):
    return len(self._dict)

  def __hash__(self):
    if self._hash is None:
      self._hash = hash(frozenset(self._dict.items()))
    return self._hash

  def __repr__(self):
    return '{}({})'.format(type(self).__name__, repr(self._dict))
