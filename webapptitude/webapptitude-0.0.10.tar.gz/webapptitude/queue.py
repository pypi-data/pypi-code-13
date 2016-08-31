"""
Queue abstraction for processing asynchronous jobs of unknown step length.

This provides the notion of "flow", wherein a single task may _yield_
additional tasks to be executed immediately thereafter, before the next task
in the initially declared series.

This module is inspired in part by the work of @kaste, in the "waterf" module.
This module DOES NOT provide strong controls to support true parallelism. Its
design is oriented to workloads which by nature require serial handling.

Usage:

    from webapptitude import queue

    series = queue.queue([
            queue.task(my_method, args...),
            queue.task(next_step_method, args...),
            queue.task(finishing_method, args...)
        ],

        # optional: when True, executes recursively in a single thread.
        immediate=False
    )

    queue.enqueue(  # start execution (possibly deferred)
        start=1  # optional: set the initial state before the first task
    )

This module is most beneficial when, for example, `my_method` would produce
additional work that must be completed before `next_step_method` should run.

A task function can perform in a variety of ways:

    def my_method(*args):
        # Enqueue another task to run immediately subsequent to this.
        # Yielding multiple in a single pass may support parallelism if the
        # deferred queue ("default") is configured appropriately. Keep in mind
        # that subsequent jobs may be enqueued/executed on completion of the
        # first of these; state locking may become sensitive.
        yield queue.task(my_method, next_args...)
        yield queue.task(my_method, another_step_args...)

        # Append a result to this job series' state.
        yield len(args)  # any value, even None, will be stored.

    def my_method(*args):
        return queue.task(my_method)  # enqueue one more task.

    def my_method(*args):
        # store this value as the job's state (any value except None)
        # overriding any series of results preceding.
        return len(args)

    def my_method(*args):
        def _inner_method(entry):
            # perform some operations on the entire job state.
            # `entry` is a {queue.Flow} instance, with a property `entry.state`
            # which will usually be a list of the preceding results. This
            # may be freely manipulated, and the `flowrunner` will enforce
            # locking accordingly. This locking DOES NOT enforce *correct*
            # serial execution, rather just that no two jobs should simultan-
            # eously modify a single state.

            # (this can behave as the generator demonstrated above.)
            yield queue.task(...)  # enqueue another task.

        return _inner_method


The "state" of a job is considered to be represented as a list of the values
produced by each task; a task series produces a series of values. These values
may then be aggregated and/or transformed, and stored again for subsequent
tasks. When a task uses `return` to override the job state, it's wrapped as a
list if necessary, to support subsequent jobs appending to it.

Once a flow is complete, it will be "sealed", and its value can be accessed as:

    >>> sequence = queue.queue(...)  # then enqueued/executed
    >>> assert (sequence.result.sealed is True)
    >>> assert (sequence.result.locked is False)
    >>> sequence.result.state


"""
from collections import namedtuple

from google.appengine.ext import deferred
from google.appengine.ext import ndb

import contextlib
import random
import time
import logging
import re
import types
import webapp2
import pickle
import traceback

DEFAULT_QUEUE = deferred.deferred._DEFAULT_QUEUE
MOCK_REQUEST = None
RE_INVALID_JOBNAME_CHARS = re.compile(r'[^a-z0-9\-]+')

CURRENT_TASK_HEADER = 'X-AppEngine-TaskName'
PREVIOUS_TASK_HEADER = 'X-AppEngine-TaskName-Previous'
TARGET_TASK_HEADER = 'X-AppEngine-TaskName-Target'


def current_request():
    """Allow requests to be mocked during test."""
    return MOCK_REQUEST or webapp2.get_request()


def get_header(header_name, default=None):
    """Shortcut for fetching header values from the current request."""
    return (current_request().headers.get(header_name, default)) or None


def sanitize_job_id(base):
    """Clean the job name to ensure compatibility with GAE's task model."""
    return RE_INVALID_JOBNAME_CHARS.sub('-', base)


def generate_job_id(callback):
    """Generate a (random/unique) name from a given method."""
    return sanitize_job_id('{module}-{method}-{rand}-{timestamp}'.format(
        module=callback.__module__,
        method=callback.__name__,
        rand=random.randint(1E3, 1E6),
        timestamp=time.time()
    ))


class Flow(ndb.Model):
    """Storage model for results/state of a series of tasks."""

    start_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update = ndb.DateTimeProperty(auto_now=True)
    locked = ndb.BooleanProperty(default=False)
    sealed = ndb.BooleanProperty(default=False)
    # PickleProperty must NOT be indexed, else limited to 1500 bytes
    state = ndb.PickleProperty(indexed=False, compressed=True)

    @property
    def current_task_id(self):  # NB no longer used in tracking state.
        """Identity of the currently executing job."""
        return get_header(CURRENT_TASK_HEADER)

    @property
    def previous_task_id(self):  # NB no longer used in tracking state.
        """Possible identity of an ancestor job."""
        return get_header(PREVIOUS_TASK_HEADER)

    @property
    def target_task_id(self):  # NB no longer used in tracking state.
        """Identify the state/results for the current job."""
        return get_header(TARGET_TASK_HEADER) or \
            self.previous_task_id or \
            self.current_task_id

    @classmethod
    @ndb.transactional
    @contextlib.contextmanager
    def locker(cls, job_id, enforce_locking=True):
        """Provide a safe context to retain job state and manage locks."""
        assert ((job_id is not None) and bool(job_id))
        entry = cls.get_or_insert(job_id, state=[])
        if (entry.locked and enforce_locking):
            # NB a bypass so "immediate" mode can avoid lock conflicts within
            # a (single-thread) sequence.
            raise ValueError("Flow is locked (%r)" % (job_id))
        try:
            entry.locked = True
            entry.put_async()
            yield entry
        finally:
            # logging.info('Storing value %r' % (entry.state,))
            entry.locked = False
            entry.put()

    @classmethod
    def state_of(cls, job_id):
        """Retrieve the state of a given job by ID."""
        assert (job_id is not None), "The job ID must not be None"
        entry = cls.get_by_id(job_id)
        if entry is None:
            return False, None  # not locked, no result
        else:
            return entry.locked, entry.state

    @classmethod
    def previous_result(cls):
        state = cls.state_of(get_header(PREVIOUS_TASK_HEADER))
        locked, result = state
        assert (not locked), "The requested (previous) result is locked!"
        return result

    @classmethod
    def current_state(cls):
        return cls.state_of(get_header(TARGET_TASK_HEADER))



class PickleMethod(object):

    def __init__(self, *parts):
        self.parts = parts

    def __call__(self, *args, **kwargs):
        return getattr(*self.parts)(*args, **kwargs)

    @property
    def __name__(self):
        return '%s.%s' % self.parts


class Task(namedtuple('Task', 'handler, args, kwargs, job_id')):

    @classmethod
    def fixbinding(cls, callback):
        """Prepare a callable (method) with bindings appropriate for pickling."""
        # Similar to the _PickableMethod and pickable() feature in `waterf.queue`
        if isinstance(callback, types.MethodType):
            return PickleMethod(callback.im_self, callback.im_func.__name__)
        elif isinstance(callback, types.BuiltinMethodType):
            if not callback.__self__:
                return callback
            else:
                return PickleMethod(callback.__self__, callback.__name__)
        elif isinstance(callback, types.ObjectType) and \
                hasattr(callback, '__call__'):
            return callback
        elif isinstance(callback, (types.FunctionType, types.BuiltinFunctionType,
                                   types.ClassType, types.UnboundMethodType)):
            return callback
        else:
            raise ValueError("Unpicklable method. %r" % (callback))

    def __call__(self, *args, **kwargs):
        # handler = self.handler
        return self.handler(*self.args, **self.kwargs)


def task(handler, *args, **kwargs):
    """Constructor proxy for task entries."""
    handler = Task.fixbinding(handler)
    job_id = (generate_job_id(handler) + '-t')
    return Task(handler, args, kwargs, job_id)

def stateful_task(handler, *args, **kwargs):
    job_id = generate_job_id(handler) + '-s'
    handler = Task.fixbinding(handler)
    return Task(fetch_state, [handler] + list(args), kwargs, job_id)


def is_callable_task(item):
    """Complete assurance that the thing matches our task pattern."""
    return isinstance(item, Task) and \
        len(item) == 4 and \
        callable(item[0]) and \
        isinstance(item[3], basestring) and \
        isinstance(item[1], (tuple, list)) and \
        isinstance(item[2], dict)


def fetch_state(callback, *args, **kwargs):
    """Delegate the current job state entry to a derivative method."""
    return callback


def next_task_headers():
    """Standard header dictionary for enqueuing the next job."""
    return {(PREVIOUS_TASK_HEADER): get_header(CURRENT_TASK_HEADER)}


def flowrunner(task_instance, key, done=None, fail=None, immediate=False):
    assert is_callable_task(task_instance)
    assert isinstance(key, basestring)
    # handler, args, kwargs, job_id = task_instance
    extended = False

    # logging.info("Processing flow %r & %r" % (key, task_instance))

    def notify_failure(err):
        logging.debug('Flow error: %r (%s)' % (err, err))
        if is_callable_task(fail):
            if immediate:
                flowrunner(fail, key, immediate=immediate)
            else:
                deferred.defer(flowrunner, fail, key,
                               _name=fail[3], _headers=next_task_headers())

    # NB when a flow is run in "immediate" mode, the (effective)
    # recursion of the task sequence results in lock release being
    # deferred until all tasks have completed. Therefore locking is
    # simply not enforced in "immediate" mode.
    with Flow.locker(key, enforce_locking=(not immediate)) as entry:
        try:
            result = task_instance()
            # result = handler(*args, **kwargs)
        except Exception, e:
            notify_failure(e)
            raise

        if isinstance(result, (types.FunctionType, types.MethodType)):
            # returned a callback?!
            # This scenario may return (again) a callable task, evaluated below
            try:
                result = result(entry)
            except Exception, e:
                notify_failure(e)
                raise

        if isinstance(result, types.GeneratorType):
            try:
                for value in iter(result):
                    if is_callable_task(value):  # extends the current task
                        extended = True
                        if immediate:
                            flowrunner(value, key, done=done, fail=fail,
                                       immediate=True)
                        else:
                            deferred.defer(flowrunner, value, key,
                                           done=done, fail=fail,
                                           _headers=next_task_headers())
                    else:
                        # logging.info('Appending result %r' % (value,))
                        entry.state.append(value)
            except Exception, e:
                notify_failure(e)
                raise
            finally:
                result = None

        # The handler (or perhaps a delegate callback) may return another task
        if is_callable_task(result):  # extends the current task
            extended = True
            if immediate:
                flowrunner(result, key, done=done, fail=fail, immediate=True)
            else:
                deferred.defer(flowrunner, result, key, done=done, fail=fail,
                               _headers=next_task_headers())
        elif (result is not None) and not (callable(result)):
            # Jobs that "return" (are not generators) should override the
            # existing state, however to support subsequent tasks it must
            # be retained as a list.
            if not isinstance(result, list):
                result = [result]
            entry.state = result

        # No subsequent tasks were enqueued, so we can terminate.
        if not extended and is_callable_task(done):
            if immediate:
                flowrunner(done, key, fail=fail, immediate=True)
            else:
                deferred.defer(flowrunner, done, key, fail=fail,
                               _name=done.job_id,
                               _headers=next_task_headers())


class _DeferredSequence(object):

    def __init__(self, jobs, **options):
        self.jobs = jobs
        self.options = options
        self.task_id = options.pop('name', generate_job_id(self.__call__))
        self.immediate = bool(options.pop('immediate', False))

    @property
    def __name__(self):
        return self.task_id

    @property
    def name(self):
        return self.task_id

    def complete(self):
        def _done(entry):
            # logging.info("Setting seal to result %r" % (entry))
            entry.sealed = True
        return _done

    def failure(self):
        # logging.error("Something went terribly wrong.")
        pass

    def seed_value(self, base):
        """Provide a starting value for the current job."""
        return Flow.get_or_insert(self.task_id, state=[base])

    @property
    def _done(self):
        return task(self.options.get('done', self.complete))

    @property
    def _fail(self):
        return task(self.options.get('fail', self.failure))

    @property
    def result(self):
        return Flow.get_by_id(self.task_id)

    def enqueue_job(self, job, last=False):
        kwargs = dict(fail=self._fail)
        if not last:
            kwargs['done'] = task(self)

        if self.immediate:
            kwargs['immediate'] = True
            flowrunner(job, self.task_id, **kwargs)
        else:
            kwargs['_headers'] = (kwargs.pop('headers', next_task_headers()))
            deferred.defer(flowrunner, job, self.task_id, **kwargs)

    def __call__(self):
        """
        Begin (or continue) execution of the current job series.

        This function must NOT return. Doing so alters flow state in the
        flowrunner process above, when it evaluates the results.
        """
        if len(self.jobs):
            job = self.jobs.pop(0)
            self.enqueue_job(job, last=False)
        else:
            self.enqueue_job(self._done, last=True)

    def enqueue(self, *args, **kwargs):
        base = kwargs.pop('start', None)
        if base is not None:
            # set the initial state if provided.
            self.seed_value(base)
        if self.immediate:
            self()
            return self
        else:
            return deferred.defer(self, *args, **kwargs)

queue = _DeferredSequence
