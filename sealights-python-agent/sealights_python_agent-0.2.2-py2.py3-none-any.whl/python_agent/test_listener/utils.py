import logging
import functools
import threading

from selenium.webdriver.remote.webdriver import WebDriver

try:
    import requests
except ImportError:
    from python_agent import requests

from python_agent.test_listener import config

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


def new_execute(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            import inspect
            self = args[0]
            frames = inspect.stack()
            for index, frame in enumerate(frames):
                current_test_identifier = StateTracker().current_test_identifier
                test_name = current_test_identifier.split("/")[1].split(" (")[0] if current_test_identifier else None
                if test_name == frame[3]:
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


def handle_requests_result(f):
    @functools.wraps(f)
    def inner_handle(*args, **kwargs):
        if StateTracker().current_test_identifier:
            headers = kwargs.get("headers", {})
            headers[config.TEST_IDENTIFIER] = StateTracker().current_test_identifier
            kwargs["headers"] = headers
        return f(*args, **kwargs)
    return inner_handle

requests.post = handle_requests_result(requests.post)
requests.get = handle_requests_result(requests.get)
