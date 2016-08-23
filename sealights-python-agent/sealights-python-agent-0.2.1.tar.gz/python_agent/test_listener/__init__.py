import uuid

from python_agent.test_listener.queues.outgoing import OutgoingMessageQueue
from python_agent.test_listener.utils import StateTracker


class TestListener(object):

    def __init__(self, customer_id, app_name, build, branch, env, server):
        self.outgoing_queue = OutgoingMessageQueue(customer_id, app_name, build, branch, env, server)
        self.execution_id = None

    def start(self):
        self.execution_id = str(uuid.uuid4())
        self.outgoing_queue.execution_started(self.execution_id)

    def stop(self):
        self.outgoing_queue.execution_ended(self.execution_id)
        self.execution_id = None

    def start_test(self, test_name):
        StateTracker().current_test_identifier = self.execution_id + "/" + test_name
        self.outgoing_queue.test_started(test_name, None, self.execution_id)

    def passed_test(self, test_name, duration):
        self.outgoing_queue.test_passed(test_name, None, self.execution_id, duration * 1000)

    def failed_test(self, test_name, duration):
        self.outgoing_queue.test_failed(test_name, None, self.execution_id, duration * 1000)

    def skipped_test(self, test_name, duration):
        self.outgoing_queue.test_skipped(test_name, None, self.execution_id, duration * 1000)

