import time


def trace(func):
    def fn(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        print('TRACE --- {} => {} ms'.format(func.__name__, 1000 * (time.time() - t)))
        return result

    return fn


def key_excep(message):
    def decor(func):
        def returnfunc(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError as e:
                print(message)
        return returnfunc
    return decor
