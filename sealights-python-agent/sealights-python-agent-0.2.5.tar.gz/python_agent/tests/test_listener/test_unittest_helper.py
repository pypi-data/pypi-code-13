import sys
import unittest

from mock import patch

from python_agent.test_listener.integrations import unittest_helper
from python_agent.test_listener import config


class SanityTestCase(unittest.TestCase):

    def test_3plus3(self):
        assert 3 + 3 == 6

    def test_1plus1(self):
        assert 1 + 1 == 2


class PassSkipTestCase(unittest.TestCase):

    def test_3plus3(self):
        self.assertEqual(3 + 3, 6)

    @unittest.skip("")
    def test_1plus1(self):
        self.assertEqual(1 + 1, 2)


class AllSkipTestCase(unittest.TestCase):

    @unittest.skip("")
    def test_3plus3(self):
        self.assertEqual(3 + 3, 6)

    @unittest.skip("")
    def test_1plus1(self):
        self.assertEqual(1 + 1, 2)


class PassErrorTestCase(unittest.TestCase):

    def test_3plus3(self):
        self.assertTrue(3 + 3 == 6)

    def test_1plus1(self):
        self.assertEqual(1 + 1, 2)


class OrchestratorTestCase(unittest.TestCase):

    def setUp(self):
        self.agent_params = {
            "customer_id": "customer",
            "app_name": "agent",
            "server": "http://someserver/api"
        }

    @patch("python_agent.requests.post", spec=True)
    def test_sanity(self, mock_post):
        event_types = ['executionIdStarted', 'testStart', 'testEnd', 'testStart', 'testEnd', 'executionIdEnded']
        sys.argv = [
            "python -m unittest",
            "--verbose",
            "--customer_id=%s" % self.agent_params["customer_id"],
            "--app_name=%s" % self.agent_params["app_name"],
            "--server=%s" % self.agent_params["server"],
            "python_agent.tests.test_listener.test_unittest_helper.SanityTestCase"
        ]
        try:
            unittest_helper.main()
        except SystemExit as e:
            if getattr(e, "code", True):
                raise

        self.assertEqual(mock_post.call_count, 6)
        for index, (args, kwargs) in enumerate(mock_post.call_args_list):
            self.assertEqual(args[0], self.agent_params["server"] + "/v1/testevents")
            message = kwargs.get("json", {})
            self.assertEqual(message.get("customerId", ""), self.agent_params["customer_id"])
            self.assertEqual(message.get("appName", ""), self.agent_params["app_name"])
            self.assertEqual(message.get("branch", ""), "master")
            self.assertEqual(message.get("build", ""), "1")
            events = message.get("events", [])
            self.assertTrue(events)
            self.assertEqual(events[0].get("type"), event_types[index])
            if events[0].get("type") == "testEnd":
                self.assertEqual(events[0].get("result"), "passed")

    @patch("python_agent.requests.post", spec=True)
    def test_pass_skip(self, mock_post):
        sys.argv = [
            "python -m unittest",
            "--verbose",
            "--customer_id=%s" % self.agent_params["customer_id"],
            "--app_name=%s" % self.agent_params["app_name"],
            "--server=%s" % self.agent_params["server"],
            "python_agent.tests.test_listener.test_unittest_helper.PassSkipTestCase"
        ]
        try:
            unittest_helper.main()
        except SystemExit as e:
            if getattr(e, "code", True):
                raise
        self.assertEqual(mock_post.call_count, 6)

        call_args = mock_post.call_args_list
        for call_arg in call_args:
            event = call_arg[1]["json"]["events"][0]
            if event.get("type") == "testEnd" and "test_3plus3" in event.get("testName", ""):
                self.assertEqual(event.get("result"), "passed")
            if event.get("type") == "testEnd" and "test_1plus1" in event.get("testName", ""):
                self.assertEqual(event.get("result"), "skipped")

    @patch("python_agent.requests.post", spec=True)
    def test_all_skip(self, mock_post):
        sys.argv = [
            "python -m unittest",
            "--verbose",
            "--customer_id=%s" % self.agent_params["customer_id"],
            "--app_name=%s" % self.agent_params["app_name"],
            "--server=%s" % self.agent_params["server"],
            "python_agent.tests.test_listener.test_unittest_helper.AllSkipTestCase"
        ]
        try:
            unittest_helper.main()
        except SystemExit as e:
            if getattr(e, "code", True):
                raise
        self.assertEqual(mock_post.call_count, 6)
        call_args = mock_post.call_args_list
        for call_arg in call_args:
            event = call_arg[1]["json"]["events"][0]
            if event.get("type") == "testEnd":
                self.assertEqual(event.get("result"), "skipped")

    @patch("python_agent.requests.post", spec=True)
    def test_pass_error(self, mock_post):
        with patch("unittest.TestCase.assertEqual", spec=True) as mock_assert_equal:
            mock_assert_equal.side_effect = Exception()
            sys.argv = [
                "python -m unittest",
                "--verbose",
                "--customer_id=%s" % self.agent_params["customer_id"],
                "--app_name=%s" % self.agent_params["app_name"],
                "--server=%s" % self.agent_params["server"],
                "python_agent.tests.test_listener.test_unittest_helper.PassErrorTestCase"
            ]
            try:
                unittest_helper.main()
            except SystemExit:
                pass

        self.assertEqual(mock_post.call_count, 6)

        call_args = mock_post.call_args_list
        for call_arg in call_args:
            event = call_arg[1]["json"]["events"][0]
            if event.get("type") == "testEnd" and "test_3plus3" in event.get("testName", ""):
                self.assertEqual(event.get("result"), "passed")
            if event.get("type") == "testEnd" and "test_1plus1" in event.get("testName", ""):
                self.assertEqual(event.get("result"), "failed")

    @patch("python_agent.requests.post", spec=True)
    def test_pass_failure(self, mock_post):
        with patch("unittest.TestCase.assertEqual", spec=True) as mock_assert_equal:
            mock_assert_equal.side_effect = AssertionError
            sys.argv = [
                "python -m unittest",
                "--verbose",
                "--customer_id=%s" % self.agent_params["customer_id"],
                "--app_name=%s" % self.agent_params["app_name"],
                "--server=%s" % self.agent_params["server"],
                "python_agent.tests.test_listener.test_unittest_helper.PassErrorTestCase"
            ]
            try:
                unittest_helper.main()
            except SystemExit:
                pass
        self.assertEqual(mock_post.call_count, 6)

        call_args = mock_post.call_args_list
        for call_arg in call_args:
            event = call_arg[1]["json"]["events"][0]
            if event.get("type") == "testEnd" and "test_3plus3" in event.get("testName", ""):
                self.assertEqual(event.get("result"), "passed")
            if event.get("type") == "testEnd" and "test_1plus1" in event.get("testName", ""):
                self.assertEqual(event.get("result"), "failed")

    @patch("python_agent.test_listener.TestListener.start", spec=True)
    @patch("python_agent.requests.post", spec=True)
    def test_execution_start_fail(self, mock_post, mock_start):
        event_types = ['testStart', 'testEnd', 'testStart', 'testEnd', 'executionIdEnded']
        mock_start.side_effect = Exception()
        sys.argv = [
            "python -m unittest",
            "--verbose",
            "--customer_id=%s" % self.agent_params["customer_id"],
            "--app_name=%s" % self.agent_params["app_name"],
            "--server=%s" % self.agent_params["server"],
            "python_agent.tests.test_listener.test_unittest_helper.SanityTestCase"
        ]
        try:
            unittest_helper.main()
        except SystemExit as e:
            if getattr(e, "code", True):
                raise
        self.assertEqual(mock_post.call_count, 5)
        call_args = mock_post.call_args_list
        for index, call_arg in enumerate(call_args):
            event = call_arg[1]["json"]["events"][0]
            self.assertEqual(event.get("type"), event_types[index])

    @patch("python_agent.test_listener.TestListener.stop", spec=True)
    @patch("python_agent.requests.post", spec=True)
    def test_execution_end_fail(self, mock_post, mock_stop):
        event_types = ['executionIdStarted', 'testStart', 'testEnd', 'testStart', 'testEnd']
        mock_stop.side_effect = Exception()
        sys.argv = [
            "python -m unittest",
            "--verbose",
            "--customer_id=%s" % self.agent_params["customer_id"],
            "--app_name=%s" % self.agent_params["app_name"],
            "--server=%s" % self.agent_params["server"],
            "python_agent.tests.test_listener.test_unittest_helper.SanityTestCase"
        ]
        try:
            unittest_helper.main()
        except SystemExit as e:
            if getattr(e, "code", True):
                raise
        self.assertEqual(mock_post.call_count, 5)
        call_args = mock_post.call_args_list
        for index, call_arg in enumerate(call_args):
            event = call_arg[1]["json"]["events"][0]
            self.assertEqual(event.get("type"), event_types[index])

    @patch("python_agent.test_listener.TestListener.start_test", spec=True)
    @patch("python_agent.requests.post", spec=True)
    def test_test_start_fail(self, mock_post, mock_start_test):
        event_types = ['executionIdStarted', 'testEnd', 'testEnd', 'executionIdEnded']
        mock_start_test.side_effect = Exception()
        sys.argv = [
            "python -m unittest",
            "--verbose",
            "--customer_id=%s" % self.agent_params["customer_id"],
            "--app_name=%s" % self.agent_params["app_name"],
            "--server=%s" % self.agent_params["server"],
            "python_agent.tests.test_listener.test_unittest_helper.SanityTestCase"
        ]
        try:
            unittest_helper.main()
        except SystemExit as e:
            if getattr(e, "code", True):
                raise
        self.assertEqual(mock_post.call_count, 4)
        call_args = mock_post.call_args_list
        for index, call_arg in enumerate(call_args):
            event = call_arg[1]["json"]["events"][0]
            self.assertEqual(event.get("type"), event_types[index])

    @patch("python_agent.test_listener.TestListener.passed_test", spec=True)
    @patch("python_agent.requests.post", spec=True)
    def test_passed_test_fail(self, mock_post, mock_passed_test):
        event_types = ['executionIdStarted', 'testStart', 'testStart', 'executionIdEnded']
        mock_passed_test.side_effect = Exception()
        sys.argv = [
            "python -m unittest",
            "--verbose",
            "--customer_id=%s" % self.agent_params["customer_id"],
            "--app_name=%s" % self.agent_params["app_name"],
            "--server=%s" % self.agent_params["server"],
            "python_agent.tests.test_listener.test_unittest_helper.SanityTestCase"
        ]
        try:
            unittest_helper.main()
        except SystemExit as e:
            if getattr(e, "code", True):
                raise
        self.assertEqual(mock_post.call_count, 4)
        call_args = mock_post.call_args_list
        for index, call_arg in enumerate(call_args):
            event = call_arg[1]["json"]["events"][0]
            self.assertEqual(event.get("type"), event_types[index])

    @patch("python_agent.test_listener.TestListener.skipped_test", spec=True)
    @patch("python_agent.requests.post", spec=True)
    def test_skipped_test_fail(self, mock_post, mock_skipped_test):
            mock_skipped_test.side_effect = Exception()
            sys.argv = [
                "python -m unittest",
                "--verbose",
                "--customer_id=%s" % self.agent_params["customer_id"],
                "--app_name=%s" % self.agent_params["app_name"],
                "--server=%s" % self.agent_params["server"],
                "python_agent.tests.test_listener.test_unittest_helper.PassSkipTestCase"
            ]
            try:
                unittest_helper.main()
            except SystemExit as e:
                if getattr(e, "code", True):
                    raise
            self.assertEqual(mock_post.call_count, 5)
            call_args = mock_post.call_args_list
            for index, call_arg in enumerate(call_args):
                event = call_arg[1]["json"]["events"][0]
                if event.get("type") == "testEnd":
                    self.assertTrue("test_3plus3" in event.get("testName", ""))

    @patch("python_agent.test_listener.TestListener.failed_test", spec=True)
    @patch("python_agent.requests.post", spec=True)
    def test_failed_test_fail(self, mock_post, mock_failed_test):
            with patch("unittest.TestCase.assertEqual", spec=True) as mock_assert_equal:
                mock_assert_equal.side_effect = Exception()
                mock_failed_test.side_effect = Exception()
                sys.argv = [
                    "python -m unittest",
                    "--verbose",
                    "--customer_id=%s" % self.agent_params["customer_id"],
                    "--app_name=%s" % self.agent_params["app_name"],
                    "--server=%s" % self.agent_params["server"],
                    "python_agent.tests.test_listener.test_unittest_helper.PassErrorTestCase"
                ]
                try:
                    unittest_helper.main()
                except SystemExit as e:
                    pass
            self.assertEqual(mock_post.call_count, 5)
            call_args = mock_post.call_args_list
            for index, call_arg in enumerate(call_args):
                event = call_arg[1]["json"]["events"][0]
                if event.get("type") == "testEnd":
                    self.assertTrue("test_1plus1" not in event.get("testName", ""))

    @patch("requests.Response", spec=True)
    @patch("python_agent.test_listener.config.app", spec=True, wraps=config.app)
    @patch("python_agent.requests.get", spec=True)
    @patch("python_agent.requests.post", spec=True)
    def test_config_from_server(self, mock_post, mock_get, mock_config, mock_response):
        mock_config.__getitem__ = lambda self, x: config.app.get(x)
        mock_response.json.return_value = {
            'meta': {
                'query': 'Python',
                'generated': '2016-08-29T14:33:34.852Z',
                'version': '1.7.265',
                'customerId': 'nutanix'
            },
            'config': '{"featuresData.enableSendLogs":true}'
        }
        mock_get.return_value = mock_response
        sys.argv = [
            "python -m unittest",
            "--verbose",
            "--customer_id=%s" % self.agent_params["customer_id"],
            "--app_name=%s" % self.agent_params["app_name"],
            "--server=%s" % self.agent_params["server"],
            "python_agent.tests.test_listener.test_unittest_helper.PassSkipTestCase"
        ]
        try:
            unittest_helper.main()
        except SystemExit as e:
            if getattr(e, "code", True):
                raise

        self.assertEqual(mock_config.get("featuresData.enableSendLogs"), True)
        self.assertEqual(mock_get.call_count, 1)
