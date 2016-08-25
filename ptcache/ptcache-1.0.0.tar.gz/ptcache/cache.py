import inspect
import hashlib
import logging
from functools import wraps

from base import singleton


def is_method(func):
    args = inspect.getargspec(func).args
    return bool(args and args[0] == 'self')


def get_func_default_kws(func, **kwargs):
    kw = {}
    inspect_args = inspect.getargspec(func)
    if inspect_args.defaults:
        kw = dict(zip(inspect_args.args[-len(inspect_args.defaults):],
                      inspect_args.defaults))
    kw.update(kwargs)
    return kw


def mark_key(func, *args, **kwargs):
    key = '%s:%s' % (func.__module__, func.__name__)
    kw = get_func_default_kws(func, **kwargs)

    if len(args) > 0:
        if is_method(func):
            args = args[1:]     # remove `self`

        for arg in args:
            v = repr(arg) if callable(arg) else str(arg)
            key += ":%s" % v
    if kw:
        for k, v in kw.items():
            v = repr(v) if callable(v) else str(v)
            key += "(%s:%s)" % (k, v)

    return hashlib.sha1(key).hexdigest()


@singleton
class Cache(object):
    def __init__(self, cache):
        self.cache = cache

    def cached(self, timeout=None):
        def wrapper(func):
            @wraps(func)
            def call(*args, **kwargs):
                key = mark_key(func, *args, **kwargs)
                rv = self.cache.get(key)
                if rv is None:
                    rv = func(*args, **kwargs)
                    if rv is not None:
                        self.cache.set(key, rv, timeout=timeout)

                return rv
            return call
        return wrapper

    def remove_cache(self, cached_method, *args, **kwargs):
        key = mark_key(cached_method, *args, **kwargs)
        self.cache.delete(key)

    def uncache(self, cached_method, arg_indexs=None, kwarg_names=None):
        def wrapper(func):
            @wraps(func)
            def call(*args, **kwargs):
                ret = func(*args, **kwargs)
                try:
                    kw = get_func_default_kws(func, **kwargs)
                    arg_list = [args[i] for i in arg_indexs] if arg_indexs else args
                    kwarg_list = dict([(k, kw[k]) for k in kwarg_names]) \
                        if kwarg_names else kw

                    self.remove_cache(cached_method, *arg_list, **kwarg_list)
                except Exception as ex:
                    logging.error(ex)
                return ret
            return call
        return wrapper
