from .error import LevelError

def applyto (func, obj, level) :
    if (level == 0) :
        func(obj)
        return

    if (isinstance(obj, list) or isinstance(obj, tuple)) :
        for i in range(0, len(obj)) :
            applyto(func, obj[i], level - 1)
        return

    if (isinstance(obj, dict)) :
        for key in obj.keys() :
            applyto(func, obj[key], level - 1)
        return
    raise LevelError()
