from pyfunk import collections as __, combinators as _

# Removes values that are None from the dict
# @sig remove_nones :: dict[a] -> dict[a]
remove_nones = __.ffilter(lambda x: x is not None)

# Removes values that are either None, or empty string from the dict
# @sig remove_empty :: dict[a] -> dict[a]
remove_empty = _.compose(__.ffilter(lambda x: x is not None), __.ffilter(lambda x: x != ''))


def merge_dict(obj1, obj2):
    """
    Create new dict that is a combination of the two dicts passed.
    Note that the new dict my not be in the order expected
    @sig merge_dict :: dict[a], dict[b] -> dict[ab]
    """
    tmp = obj1.copy()
    tmp.update(obj2)
    return tmp


def dict_items(obj):
    """
    Create a list of tuples(key, value) of the dict
    @sig dict_items :: dict[a] -> [(Str, a)]
    """
    return list(zip(obj.keys(), obj.values()))


@_.curry
def only(args, obj):
    '''
    Extract some properties from an object
    @sig only :: [Str] -> dict[a] -> dict[a]
    '''
    return {k: v for k, v in dict_items(obj) if k in args}


@_.curry
def but(args, obj):
    '''
    Extract all properties from an object except the given ones
    @sig but :: [Str] -> dict[a] -> dict[a]
    '''
    return {k: v for k, v in dict_items(obj) if k not in args}


def is_empty(obj):
    '''
    Confirm if there is a single shred of value in the dict
    @sig has_content :: dict[a] -> Bool
    '''
    return not(obj is None or len(obj) == 0 or len(remove_empty(obj)) == 0)
