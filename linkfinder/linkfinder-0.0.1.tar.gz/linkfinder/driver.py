from gevent.pool import Pool
from gevent.queue import Queue

import requests
import gevent.monkey
gevent.monkey.patch_socket()


class GeventDriver(object):

    def __init__(self, size=1000):
        self.pool = Pool(size)
        self.queue = Queue()

    def call(self, endpoint):
        try:
            r = requests.head(endpoint, timeout=3.0)
            self.queue.put((r.status_code, endpoint))
        except Exception as e:
            print e.message

    def process(self, endpoints):
        # should be ok to use a list here as new events
        # are only being used to on head()not on retrieving an endpoint
        for e in endpoints:
            self.pool.spawn(self.call, e)
        self.pool.join()
