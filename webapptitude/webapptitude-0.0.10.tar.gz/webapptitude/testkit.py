
import unittest
import traceback
import sys
import os
import pdb
import cStringIO
import base64

# from google.appengine.api import memcache
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from google.appengine.api import apiproxy_stub_map

import webob
import webapp2
import webtest
import logging
import contextlib

from webtest.http import StopableWSGIServer

from util import odict

try:
    from appengine_config import config as site_config
except ImportError:
    site_config = {}
    site_config["webapp2_extras.sessions"] = {
        "secret_key": "TEST_SESSION_SECRET"
    }


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def environ_base64_buffer(name, default=None):
    """
    Read an environment variable, decode as base64, then render as a buffer.

    In some testing environments, sensitive information may be available as
    environment variables, encoded as base64 for compatibility. This provides
    a simple way to read them as though they were files.
    """
    value = os.environ.get(name, default)
    if isinstance(value, basestring):
        value = cStringIO.StringIO(base64.b64decode(value))
    return value


@contextlib.contextmanager
def debug_with(*exceptions):
    try:
        yield
    except exceptions:
        info = sys.exc_info()
        traceback.print_exception(*info)
        pdb.post_mortem(info[2])
    finally:
        pass


def debug_on(*exceptions):
    def _decorate(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions:
                info = sys.exc_info()
                traceback.print_exception(*info)
                pdb.post_mortem(info[2])
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        return wrapper

    if len(exceptions) == 0:
        exceptions = (AssertionError,)
    return _decorate


class Testbed(testbed.Testbed):

    service_alias = {  # stub identifiers for common named services
        'ndb': 'datastore_v3',
        'datastore': 'datastore_v3',
        'identity': 'app_identity_service',
        'capability': 'capability_service'
    }

    def prepare(self, **kwargs):
        selected_stubs = kwargs.pop('stubs', None)
        app_path = kwargs.pop('apppath', None)

        if isinstance(app_path, basestring):
            if app_path.endswith('app.yaml'):
                app_path = app_path[:-8]
        else:
            app_path = os.path.dirname(os.path.dirname(__file__))

        self.activate()
        self.setup_env(overwrite=True, **kwargs)

        if selected_stubs is None:
            self.init_all_stubs()
        elif isinstance(selected_stubs, list):
            for stub in selected_stubs:
                self._init_stub(self.service_alias.get(stub, stub))

        if kwargs.pop('taskqueue', True):
            # This will fail when the taskqueue stub is not initialized.
            # This can happen when (for example) the 'stubs' arg is False.
            # taskqueue = apiproxy_stub_map.apiproxy.GetStub('taskqueue')
            taskqueue = self.get_stub('taskqueue')
            if taskqueue is not None:
                taskqueue._root_path = app_path

    @property
    def taskqueue_stub(self):
        return self.get_stub(testbed.TASKQUEUE_SERVICE_NAME)

    def loginUser(self, email='test@example.com', id='123', is_admin=False):
        self.setup_env(
            user_email=str(email), user_id=str(id),
            user_is_admin=('1' if is_admin else '0'),
            overwrite=True
        )

    def loginAnonymous(self):
        self.loginUser(email="", id=0, is_admin=False)




class TestCase(unittest.TestCase):
    logger = logger
    noisy = False
    stubs = None
    stub_config = None

    @classmethod
    def application(cls, instance):
        """Construct a test application from an existing WSGI application."""
        assert isinstance(instance, webapp2.WSGIApplication)
        return webtest.TestApp(instance)

    @classmethod
    def application_from(cls, *handlers):
        """Construct a suitable test application from a mapping of handlers."""
        return cls.application(
            webapp2.WSGIApplication(handlers,
                                    config=site_config,
                                    debug=True)
        )

    @classmethod
    def notice(cls, message):
        if cls.noisy:
            cls.logger.warn(message)
        # print >>sys.stderr, message

    @classmethod
    @contextlib.contextmanager
    def prepare_webservice(cls, instance):
        """
        Spawn a thread for an application instance; this can be useful when a
        test utility requires reaching a TCP service, rather than passing
        calls through the WSGI standard.

        This context function yields a string, the URL root for the service
        thread, e.g. "htt://<hostname>:<port>"

        Usage:

            app = webapp2.WSGIApplication(...)

            class TestCase(helper.TestCase):

                def testRequestSomething(self):
                    result = None
                    with self.webservice as http:
                        res = requests.get(http + '/path')
                        result = res.status_code
                    self.assertEqual(result, 200)

        """
        if isinstance(instance, webtest.TestApp):
            instance = instance.app

        assert isinstance(instance, webapp2.WSGIApplication)
        server = StopableWSGIServer.create(instance)
        host = server.adj.host
        port = server.adj.port
        try:
            cls.notice("Service started on %r" % ([host, port]))
            yield 'http://%s:%s' % (host, port)
        finally:
            cls.notice("Shutting down service on %r" % ([host, port]))
            server.shutdown()

    @property
    def webservice(self):
        """Shortcut for constructing a service thread."""
        assert isinstance(self.testapp, webtest.TestApp)
        return self.prepare_webservice(self.testapp.app)


    @classmethod
    def setUpClass(cls):
        testbed_options = cls.stub_config or {}
        cls.testbed = Testbed()
        cls.testbed.prepare(stubs=cls.stubs, **testbed_options)

        app = getattr(cls, 'getHandlers', None)
        if callable(app):
            handlers = app()
            if isinstance(handlers, webapp2.WSGIApplication):
                cls.testapp = cls.application(handlers)
            else:
                cls.testapp = cls.application_from(*list(handlers))

    def tearDown(self):
        # After each test, we want the cache reset to mitigate side-effects.
        ndb.get_context().clear_cache()

    @classmethod
    def tearDownClass(cls):
        cls.testbed.deactivate()

    def iter_queue_tasks(self, *queue_names):
        """
        Execute the queue. This assumes a sequence is already enqueued.

        Because this test environment does not leverage a proper web service
        thread, we simulate the queue-runner here, until the queue is empty.
        """
        taskqueue = self.testbed.taskqueue_stub

        while True:
            tasks_performed = 0
            for q in queue_names:
                tasks = taskqueue.get_filtered_tasks(queue_names=q)
                tasks_performed = tasks_performed + len(tasks)
                logging.info('Queue runner found %d tasks' % (len(tasks)))
                for task in tasks:
                    yield q, task
            if not tasks_performed:
                break





    def assertResponse(self, response, body=None, response_code=None,
                       content_type=None):
        """Shortcut for assessing one or multiple attributes of a response."""
        self.assertIsInstance(response, webob.Response)
        if isinstance(response_code, int):
            self.assertEqual(response.status_int, response_code)
        if isinstance(response_code, (list, tuple)):
            self.assertIn(response.status_int, response_code)
        if isinstance(content_type, basestring):
            self.assertEqual(response.content_type, content_type)
        if isinstance(body, basestring):
            self.assertEqual(response.normal_body, body)


# For compatibility only...
ServiceRequestCase = type("ServiceRequestCase", (TestCase,), {})


def ApplicationTestCase(application):
    """Construct a testcase class based on an application instance."""

    @classmethod
    def handlers(cls):
        return application

    return type("TestCase_Application", (TestCase,), {'getHandlers': handlers})


