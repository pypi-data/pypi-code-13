import redis
from listener import Listener

class Myclass(object):
    def __init__(self):
        pass

    def test(self, a, b, c):
        print a, b, c

    def sum(self, a, b, c):
        print a + b + c

    def dispatch(self):
        self.dispatcher = {
            'test': self.test,
            'sum': self.sum
        }

r = redis.Redis()
client = Listener(r, ['__key*__:*'], Myclass())
client.start()

