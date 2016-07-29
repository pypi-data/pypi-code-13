import redis

from scrapy_eagle.dashboard.settings import get_config_file

redis_pool = None

def init_memory():

    global redis_pool

    _config = get_config_file()

    redis_pool = redis.ConnectionPool(
        host=_config.get('redis', 'host', fallback='127.0.0.1'),
        port=_config.getint('redis', 'port', fallback=6379),
        db=_config.getint('redis', 'db', fallback=0)
    )

def get_redis_pool():
    return redis_pool

def get_connection():

    if not redis_pool:
        init_memory()

    return redis.Redis(connection_pool=redis_pool)

def testando():
    pass