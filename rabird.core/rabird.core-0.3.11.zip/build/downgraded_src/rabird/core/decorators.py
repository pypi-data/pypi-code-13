u'''
@date 2013-8-14

@author Hong-She Liang <starofrainnight@gmail.com>

@ref http://blog.mathieu-leplatre.info/python-check-arguments-types.html
@ref http://www.python.org/dev/peps/pep-0318/
@ref https://pypi.python.org/pypi/typecheck
'''
from itertools import izip


def accepts(*argstypes, **kwargstypes):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            if len(args) > len(argstypes):
                raise TypeError(u"%s() takes at most %s non-keyword arguments (%s given)" %
                                (func.__name__, len(argstypes), len(args)))
            argspairs = list(izip(args, argstypes))
            for k, v in list(kwargs.items()):
                if k not in kwargstypes:
                    raise TypeError(
                        u"Unexpected keyword argument '%s' for %s()" % (k, func.__name__))
                argspairs.append((v, kwargstypes[k]))
            for param, expected in argspairs:
                if param is not None and not isinstance(param, expected):
                    raise TypeError(u"Parameter '%s' is not %s" %
                                    (param, expected.__name__))
            return func(*args, **kwargs)
        return wrapped
    return wrapper


def returns(rtype):
    def wrapper(f):
        def wrapped(*args, **kwargs):
            result = f(*args, **kwargs)
            if not isinstance(result, rtype):
                raise TypeError(
                    u"return value %r does not match %s" % (result, rtype))
            return result
        return wrapped
    return wrapper
