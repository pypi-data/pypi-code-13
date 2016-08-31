from google.appengine.api import taskqueue
from webapptitude.jsonkit import json_encode, json_decode

from webapp2 import RequestHandler


class PullQueueBase(taskqueue.Queue):
    name = None

    default_batch_size = 100
    default_lease_duration = 60
    repeat_failed_tasks = True

    def __init__(self, name, method=None):
        super(PullQueueBase, self).__init__(name)
        if callable(method):
            self.run = method.__get__(self, self.__class__)  # override

    @classmethod
    def task(cls, **kwargs):
        props, keys = {}, ('countdown', 'eta', 'tag', 'name')
        for k in keys:
            props[k] = kwargs.pop(k, None)
        props['method'] = 'PULL'
        return taskqueue.Task(payload=json_encode(kwargs), **props)

    def enqueue(self, *jobs, **jobopts):
        if jobs:
            super(PullQueueBase, self).add(jobs)
        if jobopts:
            super(PullQueueBase, self).add([self.task(**jobopts)])

    def run(self, *args, **kwargs):
        raise NotImplementedError

    def process(self, batch_size=None, lease_duration=None):
        if lease_duration is None:
            lease_duration = self.default_lease_duration
        if batch_size is None:
            batch_size = self.default_batch_size
        count_processed, count_failed = 0, 0
        lease = self.lease_tasks(lease_duration, batch_size)
        while len(lease) > 0:
            for task in lease:
                data = json_decode(task.payload)
                try:
                    self.run(**data)
                except:
                    count_failed = count_failed + 1
                    if self.repeat_failed_tasks:
                        continue
                else:
                    count_processed = count_processed + 1
                    self.delete_tasks(task)
                finally:
                    if not self.repeat_failed_tasks:
                        self.delete_tasks(task)
            lease = self.lease_tasks(lease_duration, batch_size)
        return count_processed

    @property
    def requesthandler(self):
        queue = self

        class QueueRequestHandler(RequestHandler):
            def get(self):
                total = queue.process()
                self.response.content_type = 'application/json'
                self.response.write('{"processed_tasks": %d}' % (total))

        return QueueRequestHandler


class PullQueue(PullQueueBase):
    pass
