import pytest
from mock import sentinel

from python_agent.test_listener import TestListener
from python_agent.test_listener import config

pytest_plugins = "pytester"


@pytest.fixture(scope="function", autouse=True)
def agent_params():
    return {
        "customer_id": "customer",
        "app_name": "agent",
        "server": "http://someserver/api"
    }


def test_sanity(testdir, agent_params, mocker):
    event_types = ['executionIdStarted', 'testStart', 'testEnd', 'testStart', 'testEnd', 'executionIdEnded']
    testdir.makepyfile(
        """
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mock_r = mocker.patch("python_agent.requests.post", spec=True)
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mock_r.call_count == 6
    for index, (args, kwargs) in enumerate(mock_r.call_args_list):
        assert args[0] == agent_params["server"] + "/v1/testevents"
        message = kwargs.get("json", {})
        assert message.get("customerId", "") == agent_params["customer_id"]
        assert message.get("appName", "") == agent_params["app_name"]
        assert message.get("branch", "") == "master"
        assert message.get("build", "") == "1"
        events = message.get("events", [])
        assert events
        assert events[0].get("type") == event_types[index]
        if events[0].get("type") == "testEnd":
            assert events[0].get("result") == "passed"
    result.assert_outcomes(passed=2)


def test_pass_skip(testdir, agent_params, mocker):
    testdir.makepyfile(
        """
        import pytest

        def test_selenium_3plus3():
            assert 3+3 == 6

        @pytest.mark.skip()
        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mock_r = mocker.patch("python_agent.requests.post", spec=True)
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mock_r.call_count == 6

    passed_test_end_event = mock_r.call_args_list[2][1]
    events = passed_test_end_event.get("json", {}).get("events")
    assert events
    assert events[0].get("result") == "passed"

    skipped_test_end_event = mock_r.call_args_list[4][1]
    events = skipped_test_end_event.get("json", {}).get("events")
    assert events
    assert events[0].get("result") == "skipped"

    result.assert_outcomes(passed=1, skipped=1)


def test_all_skipped(testdir, agent_params, mocker):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.skip()
        def test_selenium_3plus3():
            assert 3+3 == 6

        @pytest.mark.skip()
        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mock_r = mocker.patch("python_agent.requests.post", spec=True)
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mock_r.call_count == 6

    passed_test_end_event = mock_r.call_args_list[2][1]
    events = passed_test_end_event.get("json", {}).get("events")
    assert events
    assert events[0].get("result") == "skipped"

    skipped_test_end_event = mock_r.call_args_list[4][1]
    events = skipped_test_end_event.get("json", {}).get("events")
    assert events
    assert events[0].get("result") == "skipped"

    result.assert_outcomes(skipped=2)


def test_pass_error(testdir, agent_params, mocker):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.skip()
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            a[1]
            assert 1+1 == 2
        """
    )
    mock_r = mocker.patch("python_agent.requests.post", spec=True)
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mock_r.call_count == 6

    passed_test_end_event = mock_r.call_args_list[2][1]
    events = passed_test_end_event.get("json", {}).get("events")
    assert events
    assert events[0].get("result") == "skipped"

    skipped_test_end_event = mock_r.call_args_list[4][1]
    events = skipped_test_end_event.get("json", {}).get("events")
    assert events
    assert events[0].get("result") == "failed"

    result.assert_outcomes(failed=1, skipped=1)


def test_execution_start_fail(testdir, agent_params, mocker):
    event_types = ['testStart', 'testEnd', 'testStart', 'testEnd', 'executionIdEnded']
    testdir.makepyfile(
        """
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mock_r = mocker.patch("python_agent.requests.post")
    mock_start = mocker.patch.object(TestListener, "start")
    mock_start.side_effect = Exception()
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mock_r.call_count == 5
    call_args = mock_r.call_args_list
    for index, call_arg in enumerate(call_args):
        event = call_arg[1]["json"]["events"][0]
        assert event.get("type") == event_types[index]

    result.assert_outcomes(passed=2)


def test_test_start_fail(testdir, agent_params, mocker):
    event_types = ['executionIdStarted', 'testEnd', 'testEnd', 'executionIdEnded']
    testdir.makepyfile(
        """
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mock_r = mocker.patch("python_agent.requests.post")
    mock_start_test = mocker.patch.object(TestListener, "start_test")
    mock_start_test.side_effect = Exception()
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mock_r.call_count == 4
    call_args = mock_r.call_args_list
    for index, call_arg in enumerate(call_args):
        event = call_arg[1]["json"]["events"][0]
        assert event.get("type") == event_types[index]

    result.assert_outcomes(passed=2)


def test_passed_test_fail(testdir, agent_params, mocker):
    event_types = ['executionIdStarted', 'testStart', 'testStart', 'executionIdEnded']
    testdir.makepyfile(
        """
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mock_r = mocker.patch("python_agent.requests.post")
    mock_passed_test = mocker.patch.object(TestListener, "passed_test")
    mock_passed_test.side_effect = Exception()
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mock_r.call_count == 4
    call_args = mock_r.call_args_list
    for index, call_arg in enumerate(call_args):
        event = call_arg[1]["json"]["events"][0]
        assert event.get("type") == event_types[index]

    result.assert_outcomes(passed=2)


def test_skipped_test_fail(testdir, agent_params, mocker):
    testdir.makepyfile(
        """
        import pytest

        def test_3plus3():
            assert 3+3 == 6

        @pytest.mark.skip()
        def test_1plus1():
            assert 1+1 == 2
        """
    )
    mock_r = mocker.patch("python_agent.requests.post")
    mock_skipped_test = mocker.patch.object(TestListener, "skipped_test")
    mock_skipped_test.side_effect = Exception()
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mock_r.call_count == 5
    call_args = mock_r.call_args_list
    for index, call_arg in enumerate(call_args):
        event = call_arg[1]["json"]["events"][0]
        if event.get("type") == "testEnd":
            assert "test_3plus3" in event.get("testName", "")

    result.assert_outcomes(skipped=1, passed=1)


def test_failed_test_fail(testdir, agent_params, mocker):
    testdir.makepyfile(
        """
        import pytest

        def test_3plus3():
            assert 3+3 == 6

        def test_1plus1():
            a[1]
            assert 1+1 == 2
        """
    )
    mock_r = mocker.patch("python_agent.requests.post")
    mock_failed_test = mocker.patch.object(TestListener, "failed_test")
    mock_failed_test.side_effect = Exception()
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mock_r.call_count == 5
    call_args = mock_r.call_args_list
    for index, call_arg in enumerate(call_args):
        event = call_arg[1]["json"]["events"][0]
        if event.get("type") == "testEnd":
            assert "test_3plus3" in event.get("testName", "")

    result.assert_outcomes(failed=1, passed=1)


def test_config_server(testdir, agent_params, mocker):
    testdir.makepyfile(
        """
        import pytest

        def test_selenium_3plus3():
            assert 3+3 == 6

        @pytest.mark.skip()
        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mock_get = mocker.patch("python_agent.requests.get")
    mocker.patch("python_agent.requests.post")
    mock_config = mocker.patch('python_agent.test_listener.config.app', spec=True, wraps=config.app)
    mock_config.__getitem__ = lambda self, x: config.app.get(x)
    mock_response = mocker.patch('requests.Response')
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
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mock_config.get("featuresData.enableSendLogs") is True
    assert mock_get.call_count == 1
    result.assert_outcomes(passed=1, skipped=1)
