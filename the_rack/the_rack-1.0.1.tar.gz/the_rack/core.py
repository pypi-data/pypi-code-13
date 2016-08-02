__all__ = ['Rack']

class CheckMixin:
    def check_key(self, key):
        if not isinstance(key, str):
            raise TypeError('Key must be a string.')

    def check_func_callable(self, func):
        if not callable(func):
            raise Exception('Func must be a callable.')

    def check_func_exists(self, key):
        if not self.exists(key):
            raise IndexError('Func does not exist.')

    def check_last(self, last):
        if not isinstance(last, str):
                raise Exception('No key given and no function added yet.')

class Rack(CheckMixin):
    def __init__(self):
        self.funcs = {}
        self.cache = {}
        self.factories = []
        self.last = []

    def factory(self, key=None):
        # if the given key isn't a string
        if not isinstance(key, str):
            # and last isn't one either, exception
            self.check_last(self.last)

            # if last is a string, use it as the key
            key = self.last

        self.factories.append(key)

    def set(self, key, func, factory=False):
        self.check_key(key)
        self.check_func_callable(func)

        self.funcs[key] = func
        self.last = key

        if factory == True:
            self.factory()

        return self

    def exists(self, key):
        return True if key in self.funcs else False

    def delete(self, key):
        try:
            del self.funcs[key]
            # if the funcs del fail, it can't be in factories
            self.factories.remove(key)
            # if the factories del fail, it can't be in cache
            del self.cache[key]
        except KeyError as e:
            pass
        except ValueError as e:
            pass

        return self

    def extend(self, key, func):
        self.check_func_exists(key)
        self.check_func_callable(func)

        previous = self.funcs[key]
        # remove the need to pass get in the extension lambda
        prev = lambda: previous(self.get)

        # call the callable with the get and the previous
        self.funcs[key] = lambda get: func(get, prev)

        # delete the cache
        if key in self.cache:
            del self.cache[key]

    def get(self, key):
        self.check_key(key)
        self.check_func_exists(key)

        # if cached, use it
        if key in self.cache:
            return self.cache[key]

        res = self.funcs[key](self.get)

        # if not factory, store the result in cache
        if key not in self.factories:
            self.cache[key] = res

        return res

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        if self.exists(key):
            return self.extend(key, value)

        return self.set(key, value)

    def __delitem__(self, key):
        return self.delete(key)

    def __contains__(self, item):
        return self.exists(item)
