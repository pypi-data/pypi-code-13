import collections
import icicle.FrozenDict

# TODO buffer?
already_immutable = frozenset([
  int, long, float, complex, # numeric types
  str, unicode, bytes, tuple, # sequences
  frozenset # sets
])

to_immutable = FrozenDict({
  bytearray: str, list: tuple, # sequences
  set: frozenset, # sets
  dict: FrozenDict # mappings
})

def freeze(obj):
  '''Returns an immutable copy of the object.'''
  t = type(obj)
  if t in already_immutable:
    return obj
  elif t in to_immutable:
    return to_immutable[t](obj)
  else:
    raise ValueError("type '{}' has no immutable counter-part")

def deep_freeze(obj):
  '''Deep immutable copy of the object (recursively makes immutable copies).'''
  if not isinstance(obj, collections.Iterable):
    return freeze(obj)
  items = tuple(deep_freeze(child) for child in obj)
  t = type(obj)
  if t in already_immutable:
    return t(items)
  elif t in to_immutable:
    return to_immutable[t](items)
  else:
    raise ValueError("type '{}' has no immutable counter-part")
