from webapptitude import queue
from webapptitude import testkit as helper
from webapptitude.util import odict
import logging
import contextlib
# import time
import pickle

QUEUE_STATE = odict(headers={}, empty_headers={})
queue.MOCK_REQUEST = QUEUE_STATE


@contextlib.contextmanager
def loglevel(_level):
    logger = logging.getLogger()
    restore = logger.getEffectiveLevel()
    logger.setLevel(_level)
    try:
        yield logger
    finally:
        logger.setLevel(restore)

# NOTE: this must be defined in module-scope for the `deferred` library to
# properly serialize it.
def read_page(index, data):
    if len(data) > index:
        # add an individual record to the series; this appends an entry to
        # the workflow's state.
        yield data[index]
        # a follow-on task (would-be recursion, yay!) to be executed
        # straight away, before moving to the next phase of the queue.
        yield queue.task(read_page, index + 1, data)

# NOTE: this must be defined in module-scope for the `deferred` library to
# properly serialize it.
def data_collect(entry):
    # Because this function is wrapped in queue.stateful_task(), its only
    # argument will be the Flow entry for this particular workflow series.
    data = entry.state  # all records previously obtained.
    keys, values = [], []
    for record in data:
        keys.extend(record.keys())
        values.extend(record.values())
    # returning here overrides existing state.
    return keys, values


errors = (ValueError, AssertionError, IndexError, KeyError, TypeError,
          AttributeError, pickle.PicklingError)

class QueueTestCase(helper.TestCase):

    def construct_queue(self, pages, immediate=False):

        # scans the fixture items (in stages)
        scanner = queue.task(read_page, 0, pages)

        # this will collect the results of those stages.
        finish = queue.stateful_task(data_collect)

        # Prepare the logical sequence
        result = queue.queue([scanner, finish], immediate=bool(immediate))

        assert (result is not None)
        return result

    # @helper.debug_on(*errors)
    def execute_queue(self):
        """
        Execute the queue. This assumes a sequence is already enqueued.

        Because this test environment does not leverage a proper web service
        thread, we simulate the queue-runner here, until the queue is empty.
        """
        taskqueue = self.testbed.taskqueue_stub
        queue_name = queue.DEFAULT_QUEUE
        empty_cycles = 1

        while True:
            tasks = taskqueue.get_filtered_tasks(queue_names=queue_name)
            # logging.info('Queue runner found %d tasks' % (len(tasks)))
            if len(tasks):
                # logging.info('Starting task %r' % (tasks[0].name))

                QUEUE_STATE.headers = QUEUE_STATE.empty_headers.copy()
                QUEUE_STATE.headers.update(tasks[0].headers)
                QUEUE_STATE.headers[queue.CURRENT_TASK_HEADER] = tasks[0].name

                queue.deferred.run(tasks[0].payload)
                taskqueue.DeleteTask(queue_name, tasks[0].name)
            else:
                empty_cycles = empty_cycles - 1
                if empty_cycles == 0:
                    # logging.info('Terminating queue runner.')
                    break

        # logging.info('Queue runner complete.')

    @helper.debug_on(*errors)
    def test_enqueue(self):
        # acquire the workload defined above
        fixture = [{'one': 1}, {'two': 2}, {'three': 3}]
        sequence = self.construct_queue(fixture)
        job = sequence.enqueue()

        with loglevel(logging.DEBUG):
            self.execute_queue()  # perform the configured workload

        self.assertIsInstance(job.name, basestring)

        # Because the workload is complete, we can assess its outcome
        result = sequence.result.state
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(result[0]), 2)
        self.assertSequenceEqual(result[0][0], ['one', 'two', 'three'])
        self.assertSequenceEqual(result[0][1], [1, 2, 3])


    @helper.debug_on(*errors)
    def test_immediate(self):
        # acquire the workload defined above
        fixture = [{'four': 1}, {'five': 2}, {'six': 3}]
        sequence = self.construct_queue(fixture, immediate=True)
        job = sequence.enqueue()

        self.assertIsInstance(job.name, basestring)

        # Because the workload is complete, we can assess its outcome
        result = sequence.result.state
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(result[0]), 2)
        self.assertSequenceEqual(result[0][0], ['four', 'five', 'six'])
        self.assertSequenceEqual(result[0][1], [1, 2, 3])


