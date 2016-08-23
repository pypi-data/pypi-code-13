import logging

import requests
from test_listener.utils import StateTracker

from python_agent.test_listener import config

log = logging.getLogger(__name__)


class OutgoingMessageQueue(object):

    def __init__(self, customer_id, app_name, build, branch, env):
        self.customer_id = customer_id
        self.app_name = app_name
        self.build = build
        self.branch = branch
        self.env = env

    def test_started(self, test_name, example_group, execution_id):
        event = {
            "type": "testStart",
            "testName": test_name,
            "suitPath": example_group,
            "executionId": execution_id
        }
        self.send_event(event)

    def test_passed(self, test_name, example_group, execution_id, duration):
        event = {
            "type": "testEnd",
            "testName": test_name,
            "suitPath": example_group,
            "executionId": execution_id,
            "result": "passed",
            "duration": duration
        }
        self.send_event(event)

    def test_failed(self, test_name, example_group, execution_id, duration):
        event = {
            "type": "testEnd",
            "testName": test_name,
            "suitPath": example_group,
            "executionId": execution_id,
            "result": "failed",
            "duration": duration
        }
        self.send_event(event)

    def test_skipped(self, test_name, example_group, execution_id, duration):
        event = {
            "type": "testEnd",
            "testName": test_name,
            "suitPath": example_group,
            "executionId": execution_id,
            "result": "skipped",
            "duration": duration
        }
        self.send_event(event)

    def execution_started(self, execution_id):
        event = {
            "type": "executionIdStarted",
            "framework": "python",
            "executionId": execution_id
        }
        self.send_event(event)

    def execution_ended(self, execution_id):
        event = {
            "type": "executionIdEnded",
            "executionId": execution_id
        }
        self.send_event(event)

    def send_event(self, event):
        message = {}
        message["appName"] = self.app_name
        message["customerId"] = self.customer_id
        message["environment"] = {"agentType": "python", "environmentName": self.env}
        message["events"] = [event]
        if self.branch:
            message["branch"] = self.branch
        if self.build:
            message["build"] = self.build

        url = config.server + "/v1/testevents"
        try:
            response = requests.post(
                url,
                json=message,
                headers={config.TEST_IDENTIFIER: StateTracker().current_test_identifier}
            )
            response.raise_for_status()
        except Exception as e:
            log.exception("failed sending event. url: %s. event: %s. error:%s" % (url, event, str(e)))
