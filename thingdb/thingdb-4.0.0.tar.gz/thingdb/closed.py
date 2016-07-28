try:
    from UserDict import DictMixin
except ImportError:
    from collections import MutableMapping as DictMixin

class ClosedDict(DictMixin):
    """Returns ValueError when trying to get/set/del item"""

    def closed(self, *args):
        raise ValueError('invalid operation on closed thing')
    __len__ = __getitem__ = __setitem__ = __delitem__ = __iter__ = keys = closed

    def __repr__(self):
        return '<Closed Dictionary>'