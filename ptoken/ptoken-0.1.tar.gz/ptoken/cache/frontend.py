import importlib
from ptoken.cache.backend import Backend


class Frontend:
    """
        Frontend of cache
    """
    __backend_ = None  # type: Backend

    def __init__(self, backend, **backend_kwargs):
        """

        :param backend:
            type: string
        """

        module = importlib.import_module("ptoken.cache.backend")
        self.__backend_ = getattr(module, backend)(**backend_kwargs)

    def get(self, key, default=None):
        return self.__backend_.get(key, default)

    def set(self, key, value, **kwargs):
        return self.__backend_.set(key, value, **kwargs)

    def has(self, key):
        return self.__backend_.has(key)

    def remove(self, *key):
        return self.__backend_.remove(*key)
