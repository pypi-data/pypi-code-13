from .error import LevelError

def mapto (func, obj, level) :
    if (level == 0) :
        return func(obj)

    if (isinstance(obj, list)) :
        ret = [None] * len(obj)
        for i in range(0, len(obj)) :
            ret[i] = mapto(func, obj[i], level - 1)
        return ret

    if (isinstance(obj, tuple)) :
        ret = [None] * len(obj)
        for i in range(0, len(obj)) :
            ret[i] = mapto(func, obj[i], level - 1)
        return tuple(ret)

    if (isinstance(obj, dict)) :
        ret = {}
        for key in obj.keys() :
            ret[key] = mapto(func, obj[key], level - 1)
        return ret
    raise LevelError()
