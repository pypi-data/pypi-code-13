from twisted.trial import unittest

from ooni.ui.web.server import AppRouting

class DummyRequest(object):
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val

class TestServer(unittest.TestCase):
    def test_app_routing(self):
        calls = []
        class DummyApp(object):
            app = AppRouting()

            @app.route("^/foo/(.*)$")
            def endpoint_a(self, request, value):
                calls.append((self, request, value))
                return "foo" + value

        da = DummyApp()
        self.assertEqual(da.app.execute("/foo/value", "GET", DummyRequest(1)),
                         "foovalue")
        self.assertEqual(calls, [(da, DummyRequest(1), "value")])

    def test_app_routing_with_prefix(self):
        calls = []
        class DummyApp(object):
            app = AppRouting(prefix="/api")

            @app.route("^/foo/(.*)$")
            def endpoint_a(self, request, value):
                calls.append((self, request, value))
                return "foo" + value

        da = DummyApp()
        self.assertEqual(da.app.execute("/api/foo/value", "GET",
                                        DummyRequest(1)),
                         "foovalue")
        self.assertEqual(calls, [(da, DummyRequest(1), "value")])
