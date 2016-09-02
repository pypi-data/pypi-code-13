import random
import time

from gym_vnc.twisty import reactor
from twisted.internet import defer, protocol, task
import logging

logger = logging.getLogger(__name__)
MAX_RETRIES = 10

class ConnectionTimer(protocol.Protocol):
    def connectionMade(self):
        self.transport.loseConnection()

def connection_timer_factory():
    factory = protocol.ClientFactory()
    factory.protocol = ConnectionTimer
    return factory

class StopWatch(object):
    def start(self):
        self.start_time = time.time()

    def stop(self):
        return time.time() - self.start_time

def start(endpoint):

    # Use an object for timing so that we can mutate it within the closure
    stop_watch = StopWatch()

    def success(client):
        return stop_watch.stop()

    def error(failure, retry):
        # websocketpp can fail when connections are lost too quickly
        if retry == 0:
            raise ConnectionTimerException("Max retries")
        backoff = 2 ** (MAX_RETRIES - retry + 1) + random.randint(42, 100)
        logger.error('Error connecting to websocket server - retrying in %dms - error details %s', backoff, failure)
        d = task.deferLater(reactor, backoff / 1000., go, retry - 1)
        return d

    def go(retry):
        stop_watch.start()
        factory = connection_timer_factory()
        d = endpoint.connect(factory)
        d.addCallback(success)
        d.addErrback(error, retry)
        return d

    return go(retry=MAX_RETRIES)

class ConnectionTimerException(Exception):
    pass