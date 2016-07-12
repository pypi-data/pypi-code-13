# coding=utf-8

try:
    from collections import UserList, UserDict
except ImportError:
    from UserList import UserList
    from UserDict import UserDict

import copy

__version__ = '0.4.0'


class Hook(object):
    def _before_add(self, key, item):
        """
        before add a item to the object will call this method.

        example: obj[key] = item
        """

    def _after_add(self, key, item):
        """
        like _before_add, but after add.
        """

    def _before_del(self, key, item):
        """
        before delete a item from the object will call this method.

        example: del obj[key]
        """

    def _after_del(self, key, item):
        """
        like _before_del, but after del.
        """


class List(Hook, UserList):
    """
    list like.
    """

    def __init__(self, initlist=None, hook_when_init=True):
        """

        :param initlist: iterable object
        :param hook_when_init: run hook points when it is True
        """
        UserList.__init__(self)

        if initlist:
            if hook_when_init:
                self.extend(initlist)
            else:
                self.data.extend(initlist)

    def __setitem__(self, i, item):  # x[i] = item, del and add

        if isinstance(i, slice):
            if not hasattr(item, '__contains__'):
                raise TypeError('can only assign an iterable')

            start, stop, step = i.indices(len(self))

            ########################################################
            if step == 1:
                for one in range(stop - start):
                    del self[start]

                _i = start
                for one in item:
                    self.insert(_i, one)
                    _i += 1

            else:

                if step > 1:
                    slice_size = (stop - start) // step

                    if 0 < (stop - start) % step < step:
                        slice_size += 1
                else:
                    slice_size = (start - stop) // abs(step)

                    if 0 < (start - stop) % abs(step) < abs(step):
                        slice_size += 1

                slice_size = 0 if slice_size < 0 else slice_size
                if slice_size != len(item):
                    raise ValueError('attempt to assign sequence of size {} to extended slice of size {}'.format(
                        len(item), slice_size
                    ))

                _i = start
                for one in item:
                    self[_i] = one
                    _i += step

        else:
            del self[i]
            self.insert(i, item)

    # all del action will be here
    def __delitem__(self, i):  # del x[i], del
        item = self[i]
        self._before_del(key=i, item=item)
        del self.data[i]
        self._after_del(key=i, item=item)

    def append(self, item):  # add
        self.insert(len(self), item)

    # all add action will be here
    def insert(self, i, item):
        self._before_add(key=i, item=item)
        self.data.insert(i, item)
        self._after_add(key=i, item=item)

    def pop(self, i=-1):  # del
        x = self[i]
        del self[i]
        return x

    def remove(self, item):  # del
        i = self.index(item)
        del self[i]

    def clear(self):  # del
        for i in range(len(self)):
            self.pop()

    def extend(self, other):  # add
        for item in other:
            self.append(item)

    def __iadd__(self, other):  # x += y, add
        self.extend(other)
        return self

    def __imul__(self, n):  # x *= y, add
        if not isinstance(n, int):
            raise TypeError("can't multiply sequence by non-int of type '{}'".format(type(n)))

        if n <= 0:
            self.clear()

        if n == 1:
            pass

        elif n > 1:
            old_data = copy.copy(self.data)
            for time in range(n - 1):
                self.extend(old_data)

        return self


class Dict(Hook, UserDict):
    """
    dict like.
    """
    def __init__(self, initdict=None, hook_when_init=True):
        """

        :param initdict: initialized from
        :param hook_when_init: run hook points when it is True
        """
        UserDict.__init__(self)

        if initdict:
            if hook_when_init:
                self.update(initdict)
            else:
                self.data.update(initdict)

    # all set action will be here
    def __setitem__(self, key, item):
        if key in self.keys():
            del self[key]

        self._before_add(key=key, item=item)
        self.data[key] = item
        self._after_add(key=key, item=item)

    # all del action will be here
    def __delitem__(self, key):
        item = self[key]
        self._before_del(key=key, item=item)
        del self.data[key]
        self._after_del(key=key, item=item)

    ###############################################
    # for Python 2.7 need:
    def update(self, *args, **kwargs):
        d = {}
        d.update(*args, **kwargs)
        for key, value in d.items():
            self[key] = value

    def pop(self, key, *args):
        try:
            value = self[key]
        except KeyError:
            return args
        else:
            del self[key]
            return value

    def popitem(self):
        try:
            key = next(iter(self))
        except StopIteration:
            raise KeyError
        value = self[key]
        del self[key]
        return key, value

    def __iter__(self):
        return iter(self.data)
