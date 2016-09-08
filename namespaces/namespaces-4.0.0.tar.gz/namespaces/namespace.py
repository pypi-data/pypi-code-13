from __future__ import absolute_import, unicode_literals

class Namespace(dict):
  '''A dictionary with attributes instead of keys.
  The Namespace API is inspired by collections.namedtuple.
  '''

  def __init__(self, *args, **kwargs):
    super(Namespace, self).__init__(*args, **kwargs)

  def __getattr__(self, name):
    '''Behaves similarly to collections.namedtuple#__getattr__.'''
    try:
      return self[name]
    except KeyError:
      raise AttributeError(
        "'{}' object has no attribute '{}'".format(type(self).__name__, name)
      )

  def __setattr__(self, name, value):
    self[name] = value

  def __repr__(self):
    '''Representation is a valid python expression for creating a Namespace
    (assuming contents also implement __repr__ as valid python expressions).'''
    items = ('{}={}'.format(k,repr(v)) for k,v in self.iteritems())
    return '{}({})'.format(type(self).__name__, ', '.join(items))

  def __eq__(self, other):
    return isinstance(other, type(self)) and super(self.__class__, self).__eq__(other)

  def __ne__(self, other):
    return not self == other

