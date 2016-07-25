import redis

from abc import ABCMeta, abstractclassmethod


class Backend(object):
    __metaclass__ = ABCMeta

    @abstractclassmethod
    def __init__(self, **kwargs):
        pass

    @abstractclassmethod
    def set(self, key, value, **kwargs):
        pass

    @abstractclassmethod
    def get(self, key, default=None, **kwargs):
        pass

    @abstractclassmethod
    def remove(self, **kwargs):
        pass

    @abstractclassmethod
    def has(self, key):
        pass

    @abstractclassmethod
    def remove(self, key):
        pass


class Redis(Backend):
    """
    Redis cache backend
    :pool: Redis connection
    """

    __pool = None  # type:redis.ConnectionPool

    def __init__(self, **kwargs):
        self.__create_pool(**kwargs)
        super(Redis, self).__init__(**kwargs)

    def __create_pool(self, host="127.0.0.1", password=None, db=0, port=6379, max_connections=1, force=False):
        if self.__pool is not None and force is False:
            self.__pool.disconnect()
            return

        self.__pool = redis.ConnectionPool(host=host, port=port, db=db, password=password,
                                           max_connections=max_connections)

    def get(self, key, default=None, **kwargs):
        """

        :param key:
        :param default:
        :param kwargs:
        :return:
        """
        connection = redis.Redis(connection_pool=self.__pool)
        result = connection.get(key)
        return result.decode() if result is not None else default

    def set(self, key, value, **kwargs):
        """
        Keyword Args:
            ttl (int): lifetime of key
        :param kwargs:
        :return:
        """

        connection = redis.Redis(connection_pool=self.__pool)
        if kwargs.get("ttl", None) is None:
            return connection.set(key, value)
        else:
            return connection.setex(key, value, int(kwargs.get("ttl")))

    def has(self, key):
        return not self.get(key) is None

    def remove(self, *key):
        connection = redis.Redis(connection_pool=self.__pool)
        return connection.delete(*key)
