#!/usr/bin/env python
# encoding: utf-8


class TyraelStruct(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delattr__

    def __missing__(self, key):
        return key


if __name__ == "__main__":
    args = {'a': 1, 'b': 2}
    s = TyraelStruct(args)
    print s.a
    print s.b
    s.c = "hello"
    print s.c
    s.pop('c')
    print s.c
    print s.d
