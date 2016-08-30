import logging
import Queue
import threading
from twisted.internet import defer

from gym_vnc.twisty import reactor

logger = logging.getLogger(__name__)

class ErrorBuffer(object):
    def __init__(self):
        self.queue = Queue.Queue()

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        if value != None:
            self.record(value)

    def __call__(self, error):
        self.record(error)

    def record(self, error):
        logger.debug('Error in thread %s: %s', threading.current_thread().name, error)
        error = format_error(error)

        try:
            self.queue.put_nowait(error)
        except Queue.Full:
            pass

    def check(self, timeout=None):
        if timeout is None:
            timeout = 0

        try:
            error = self.queue.get(timeout=timeout)
        except Queue.Empty:
            return
        else:
            raise error

    def blocking_check(self, timeout=None):
        # TODO: get rid of this method
        if timeout is None:
            while True:
                self.check(timeout=3600)
        else:
            self.check(timeout)


from twisted.python import failure
import traceback
import threading
from gym_vnc import error
def format_error(e):
    # errback automatically wraps everything in a Twisted Failure
    if isinstance(e, failure.Failure):
        e = e.value
    err_string = traceback.format_exc(e).rstrip()
    if err_string == 'None':
        # Reasonable heuristic for exceptions that were created by hand
        last = traceback.format_stack()[-2]
        err_string = '{}\n  {}'.format(e, last)
    # Quick and dirty hack for now.
    err_string = err_string.replace('Connection to the other side was lost in a non-clean fashion', 'Connection to the other side was lost in a non-clean fashion (HINT: this generally actually means we got a connection refused error. Check that the remote is actually running.)')
    return error.Error('Error in thread {}: cause: \n\n{}'.format(threading.current_thread().name, err_string))

def queue_get(queue):
    while True:
        try:
            result = queue.get(timeout=1000)
        except Queue.Empty:
            pass
        else:
            return result

def blockingCallFromThread(f, *a, **kw):
    queue = Queue.Queue()
    def _callFromThread():
        result = defer.maybeDeferred(f, *a, **kw)
        result.addBoth(queue.put)
    reactor.callFromThread(_callFromThread)
    result = queue_get(queue)
    if isinstance(result, failure.Failure):
        if result.frames:
            e = error.Error(str(result))
        else:
            e = result.value
        raise e
    return result

from gym import spaces
def repeat_space(space, n):
    return spaces.Tuple([space] * n)
