import logging
import numbers
import os
import threading
import time

logger = logging.getLogger(__name__)

BYTES = object()

class Error(Exception):
    pass

class RunningAverage(object):
    def __init__(self, decay=0.1):
        self.decay = decay
        self.last_update = None
        self.last_data_decay = None
        self._avg = None

    def add(self, data):
        assert isinstance(data, numbers.Number)
        if self.last_update is None:
            self._avg = data
            self.last_update = time.time()
            self.last_data_decay = 1
        else:
            now = time.time()
            delta = now - self.last_update
            if delta != 0:
                assert delta > 0, "Invalid delta value: {}".format(delta)
                self.last_data_decay = (1 - self.decay**delta) * 1/delta
                self._avg = self.decay**delta * self._avg + self.last_data_decay * data
            else:
                # Don't divide by zero; just reuse the last delta. Should stack well
                self._avg += self.last_data_decay * data
            self.last_update = now

    def avg(self):
        return self._avg

def pretty(d, unit):
    if unit == None:
        return d
    elif unit == BYTES:
        return pretty_bytes(d)
    else:
        raise Error('No such unit: {}'.format(unit))

def pretty_bytes(b):
    if b is None:
        return None

    assert isinstance(b, numbers.Number), "Surprising type for data: {} ({!r})".format(type(b), b)
    if b > 1000 * 1000:
        return '{:.0f}MB'.format(b/1000.0/1000.0)
    elif b > 1000:
        return '{:.0f}kB'.format(b/1000.0)
    else:
        return '{:.0f}B'.format(b)

def thread_id():
    return threading.current_thread().ident

class StackProfile(object):
    def __init__(self, profile):
        self.profile = profile

        self.stack_by_thread = {}
        self.lock = threading.Lock()

    def push(self, event):
        stack = self._current_stack()
        stack.append({
            'name': event,
            'start': time.time(),
        })

    def pop(self):
        stack = self._current_stack()
        event = stack.pop()
        name = event['name']
        start = event['start']

        with self.profile as txn:
            delta = time.time() - start
            txn.timing(name, delta)
            txn.incr(name + '.total_time', delta)
            txn.incr(name + '.calls')

    def _current_stack(self):
        id = thread_id()

        try:
            stack = self.stack_by_thread[id]
        except KeyError:
            with self.lock:
                # Only current thread should be adding to this entry anyway
                assert id not in self.stack_by_thread
                stack = self.stack_by_thread[id] = []
        return stack

class Profile(object):
    def __init__(self, print_frequency=None, print_filter=None):
        if print_filter is None:
            print_filter = lambda event: True

        self.lock = threading.RLock()

        self.timers = {}
        self.counters = {}

        self.print_frequency = print_frequency
        self.last_print = None

        self.print_filter = print_filter
        self._in_txn = False

    def __enter__(self):
        self.lock.acquire()
        self._in_txn = True
        return self

    def __exit__(self, type, value, tb):
        self._in_txn = False
        self._print_if_needed()
        self.lock.release()

    def timing(self, event, time):
        # return
        with self.lock:
            if event not in self.timers:
                self.timers[event] = {
                    'total_time': 0,
                    'count': 0,
                }
            self.timers[event]['total_time'] += time
            self.timers[event]['count'] += 1

            self._print_if_needed()

    def incr(self, event, amount=1, unit=None):
        # return
        with self.lock:
            if event not in self.counters:
                self.counters[event] = {'count': 0, 'rate': RunningAverage(), 'unit': unit}
            self.counters[event]['count'] += amount
            self.counters[event]['rate'].add(amount)

            self._print_if_needed()

    def _print_if_needed(self):
        """Assumes you hold the lock"""
        if self._in_txn or self.print_frequency is None:
            return
        elif self.last_print is not None and \
             self.last_print + self.print_frequency > time.time():
            return

        self.last_print = time.time()

        timers = {}
        for event, stat in self.timers.items():
            if not self.print_filter(event):
                continue

            mean = stat['total_time'] / stat['count']
            if mean < 0.001:
                mean = '{:.2f}us'.format(1000*1000*mean)
            elif mean < 1:
                mean = '{:.2f}ms'.format(1000*mean)
            else:
                mean = '{:.2f}s'.format(mean)

            timers[event] = {
                'mean': mean,
            }

        counters = {}
        as_of = time.time()
        for counter, stat in self.counters.items():
            assert isinstance(counter, str), 'Bad counter {} ({})'.format(type(counter), counter)
            if not self.print_filter(counter):
                continue

            unit = stat['unit']
            counters[counter] = {
                'count': pretty(stat['count'], unit),
                'rate': pretty(stat['rate'].avg(), unit)
            }

        # for key, value in sorted(timers.items()):
        #     logger.info('[pyprofile timer] %s=%s', key, value)

        # for key, value in sorted(counters.items()):
        #     logger.info('[pyprofile counter] %s=%s', key, value)

        logger.info('[pyprofile] timers=%s counters=%s', timers, counters)


print_frequency = os.environ.get('PYPROFILE_FREQUENCY')
if print_frequency is not None:
    print_frequency = int(print_frequency)

print_prefix = os.environ.get('PYPROFILE_PREFIX')
if print_prefix is not None:
    print_filter = lambda event: event.startswith(print_prefix)
else:
    print_filter = None

profile = Profile(print_frequency=print_frequency, print_filter=print_filter)
stack_profile = StackProfile(profile)

push = stack_profile.push
pop = stack_profile.pop
incr = profile.incr
timing = profile.timing
