# -*- coding: utf-8 -*-
import json
import logging
from functools import wraps
try:
    from django.core.serializers.json import DjangoJSONEncoder
except ImportError:
    from django.core.serializers.json import DateTimeAwareJSONEncoder as DjangoJSONEncoder


_missing = object()


class cached_property(object):
    """A decorator that converts a function into a lazy property. The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value::

        class Foo(object):

        @cached_property
        def foo(self):
            # calculate something important here
            return 42

    The class has to have a `__dict__` in order for this property to
    work.

    :copyright: (c) 2011 by the Werkzeug Team
    :license: BSD
    """

    # implementation detail: this property is implemented as non-data
    # descriptor. non-data descriptors are only invoked if there is
    # no entry with the same name in the instance's __dict__.
    # this allows us to completely get rid of the access function call
    # overhead. If one choses to invoke __get__ by hand the property
    # will still work as expected because the lookup logic is replicated
    # in __get__ for manual invocation.

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value


def capture_exception(func=None, ret=_missing, exception_class=Exception, logger=None):
    """
    Capture exception of exception_class and `ret` will be retured.
    """

    if logger and isinstance(logger, basestring):
        logger = logging.getLogger(logger)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                rv = func(*args, **kwargs)
            except Exception, e:
                if not isinstance(e, exception_class) or ret is _missing:
                    raise e
                else:
                    if logger:
                        logger.error(e)
                    rv = ret

            return rv

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


def jsonify(func=None, jsonp=None, content_type='application/json'):
    """Make view's response into JSON format"""

    from django.http import HttpResponse

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            rv = func(request, *args, **kwargs)

            if isinstance(rv, HttpResponse):
                return rv

            content = json.dumps(rv, cls=DjangoJSONEncoder,
                                 indent=None if request.is_ajax() else 2)
            if jsonp and request.GET.get(jsonp, default=None):
                fn = request.GET.get(jsonp)
                content = "%s(%s)" % (fn, content)
            response = HttpResponse(content=content, content_type=content_type)
            response['Cache-Control'] = 'no-cache'

            return response

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)
