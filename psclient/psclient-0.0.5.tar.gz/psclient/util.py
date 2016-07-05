from decorator import decorator
from time import time

from warnings import warn as _warn
def deprecated(message, allow=True):
    """Decorates a deprecated method or function with a handy warning
    message. Will log a warning exactly once."""
    warned = [False]

    @decorator
    def deprecated(func, *args, **kwargs):
        _warn(message, DeprecationWarning, stacklevel=2)
        if not warned[0]:
            _logger.warn(message)
            warned[0] = True
        if allow:
            return func(*args, **kwargs)
        else:
            raise DeprecationWarning(message)
    return deprecated

def memoize(t=None):
    """Memoizes a function to expire after t seconds.

    If t is None (default), then it never expires.
    """
    cache = {}

    @decorator
    def memoize(func, self, *args, **kwargs):
        sig = func.__name__ + str(args) + str(kwargs)
        try:
            rv, t_ = cache[sig]
            if t is None:
                return rv

            if time()-t_ < t:
                return rv
        except KeyError:
            pass

        cache[sig] = (func(self, *args, **kwargs), time())
        return cache[sig][0]

    return memoize

