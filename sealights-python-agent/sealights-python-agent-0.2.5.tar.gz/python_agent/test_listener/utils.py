import os
import logging
import logging.config
import functools
import threading
import urllib
import urllib2
import argparse
import json
from urlparse import urlparse

import pkg_resources
from selenium.webdriver.remote.webdriver import WebDriver

try:
    import requests
except ImportError:
    from python_agent import requests

from python_agent.test_listener import config
import python_agent

log = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class StateTracker(object):
    __metaclass__ = Singleton

    def __init__(self):
        self._lock = threading.Lock()
        self._current_test_identifier = None

    def __str__(self):
        if self._current_test_identifier:
            return "State: %s" % self._current_test_identifier
        return "Not in test"

    @property
    def current_test_identifier(self):
        return self._current_test_identifier

    @current_test_identifier.setter
    def current_test_identifier(self, test_id):
        self._lock.acquire()
        if self._current_test_identifier != test_id:
            self._current_test_identifier = test_id
        self._lock.release()


def identify_framework(frames):
    for frame in frames:
        if "pytest" in frame[1]:
            return "pytest"
        if "unittest" in frame[1]:
            return "unittest"


def is_test_equal_to_frame(framework, frame):
    current_test_identifier = StateTracker().current_test_identifier
    if not current_test_identifier:
        return False
    if framework == "pytest":
        test_id = urllib.url2pathname(current_test_identifier.split("/")[-1])
        file_name = frame[1].split("/")[-1] if frame[1] else ""
        test_name = frame[3] if frame[3] else ""
        return file_name + "::" + test_name == test_id
    if framework == "unittest":
        test_id = urllib.url2pathname(current_test_identifier.split("/")[-1])
        file_name_test = frame[0].f_locals["self"].id() if frame[0] else ""
        return file_name_test == test_id


def new_execute(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            import inspect
            self = args[0]
            frames = inspect.stack()
            for index, frame in enumerate(frames):
                framework = identify_framework(frames)
                if is_test_equal_to_frame(framework, frame):
                    params = {
                        "sessionId": self.session_id,
                        "cookie": {
                            "name": config.TEST_IDENTIFIER,
                            "value": StateTracker().current_test_identifier
                        }
                    }
                    self.command_executor.execute("addCookie", params)
        except Exception as e:
            log.exception("failed to set cookie. cookie: %s. error: %s"
                          % (StateTracker().current_test_identifier, str(e)))
            print str(e)
        return f(*args, **kwargs)
    return wrapper

WebDriver.execute = new_execute(WebDriver.execute)


def handle_requests(f):
    @functools.wraps(f)
    def inner_handle(*args, **kwargs):
        if StateTracker().current_test_identifier:
            headers = kwargs.get("headers", {})
            headers[config.TEST_IDENTIFIER] = StateTracker().current_test_identifier
            kwargs["headers"] = headers

        proxy = config.app["proxy"]
        if proxy:
            result = urlparse(proxy)
            if result.scheme == "https":
                os.environ["https_proxy"] = proxy
            else:
                os.environ["http_proxy"] = proxy
        return f(*args, **kwargs)
    return inner_handle

requests.post = handle_requests(requests.post)
requests.get = handle_requests(requests.get)
requests.put = handle_requests(requests.put)
requests.delete = handle_requests(requests.delete)
requests.patch = handle_requests(requests.patch)


def handle_urllib2(f):
    @functools.wraps(f)
    def inner_handle(*args, **kwargs):
        request = f(*args, **kwargs)
        if StateTracker().current_test_identifier:
            request.headers[config.TEST_IDENTIFIER] = StateTracker().current_test_identifier
        return request
    return inner_handle

urllib2.Request.__init__ = handle_urllib2(urllib2.Request.__init__)


def validate_server_api(server, is_validate_api=False):
    error_msg = "Must be of the form: http://<server>/api"
    try:
        result = urlparse(server)
        if result.scheme not in ["http", "https"]:
            raise argparse.ArgumentTypeError(error_msg)
        if is_validate_api and "/api" not in result.path:
            raise argparse.ArgumentTypeError(error_msg)
    except Exception:
        raise argparse.ArgumentTypeError(error_msg)
    return server


def validate_server(server):
    return validate_server_api(server, is_validate_api=True)


def get_config_from_server(server, customer_id, app_name, branch, env):
    server_config = {}
    url = None
    try:
        url = "/".join([server, "v1", "config", customer_id, "null", app_name, branch, env, config.app["technology"],
                        pkg_resources.require("sealights-python-agent")[0].version])
        response = python_agent.requests.get(url)
        config_data = response.json()
        config_data = config_data.get("config", "{}")
        server_config = json.loads(config_data)
        response.raise_for_status()
    except Exception as e:
        log.exception("failed getting configuration from server. url: %s. error: %s" % (url, str(e)))
    return server_config


def config_logging():
    logging.config.dictConfig(config.LOG_CONF)
    server_config = get_config_from_server(
        config.app["server"],
        config.app["customer_id"],
        config.app["app_name"],
        config.app["branch"],
        config.app["env"]
    )
    config.app.update(server_config)
    try:
        log_conf = server_config.get("logging")
        if log_conf and isinstance(log_conf, dict):
            logging.config.dictConfig(log_conf)
    except:
        log.warning("failed configuring logging for python agent. config: %s" % server_config)
