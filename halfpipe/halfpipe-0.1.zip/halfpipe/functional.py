import re, operator
import functools

class pipe_:
    def __init__(self, function):
        self.function = function
    def __rrshift__(self, other):
        return self.function(other)
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


def pipe(func):
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return pipe_(lambda *args2, **kwargs2:
                      curried(*(args + args2), **dict(kwargs, **kwargs2)))
    f = pipe_(curried)
    # f.__name__ = func.__name__
    return f 


@pipe
def default(default_value):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                return default_value
        # inner.__name__ = func.__name__
        return inner
    f = pipe(decorator)
    # f.__name__ = 
    return f

@pipe
def match_(pattern, x): 
    # print pattern
    m = re.match(pattern, x)
    return m.group(0) if m!=None else ""

@pipe
def search_(pattern, x): 
    # print pattern
    m = re.search(pattern, x)
    return m.group(0) if m!=None else ""


@pipe
def flatten(l):
    return functools.reduce(operator.add, l)

map_   = pipe(lambda x,y: map(x,y))
filter_ = pipe(lambda x,y: filter(x,y))
set_    = pipe(lambda x:set(x))
list_   = pipe(lambda x:list(x))
reduce_ = pipe(lambda x,y:functools.reduce(x,y))
int_    = pipe(lambda x:int(x))

from pandas.io.json import json_normalize
frame = pipe(lambda mg_selector:json_normalize([x for x in mg_selector]))

@pipe
def chunks(n,l):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]