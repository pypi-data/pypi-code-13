import StringIO
import unittest

try:
    import xmlrpc.client as xmlrpclib
except:
    import xmlrpclib
try:
    from mock import MagicMock
except:
    from unittest.mock import MagicMock

from supervisor_event_listeners.processrestarter import ProcessRestarter

ServerProxyMock = MagicMock(xmlrpclib.ServerProxy)


class TestProcessRestarter(unittest.TestCase):
    def test_failed_restarts(self):
        rpc = ServerProxyMock()
        stderr = StringIO.StringIO()
        restarter = ProcessRestarter(rpc, ["process"], None, None)
        restarter.stderr = stderr
        restarter._restart_processes()
        self.assertTrue(stderr.getvalue().startswith("Programs specified could not be found:"))
        self.assertTrue("process" in stderr.getvalue())
