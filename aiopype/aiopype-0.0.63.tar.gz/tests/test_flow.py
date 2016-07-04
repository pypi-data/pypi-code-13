#pylint: disable=E0401, R0201
"""
Test flow controller
"""

from unittest import mock
from unittest import TestCase

from aiopype.flow import Flow
from aiopype.manager import Manager
from aiopype.messaging import SyncEventHandler

def zero_error():
  return 1 / 0

def run_loop(loop):
  handle = loop.call_soon(zero_error)
  loop._run_once()
  return handle


class TestInit(TestCase):
  def setUp(self):
    class TestManager(Manager):
      name = 'test'
      async def stop(self):
        pass

    self.test_manager = TestManager
    config_mock = mock.Mock()
    config_mock.FLOWS = ['test']
    config_mock.RAVEN_DSN = None
    self.flow = Flow(config_mock)
    self.flow.running = True

  def test_start(self):
    loop = mock.Mock()
    loop.run_forever = mock.Mock()
    self.test_manager.start = mock.Mock(return_value = None)
    self.flow.finished = mock.Mock(return_value = "check termination condition perodically")

    self.flow.loop = loop
    self.flow.start()
    self.test_manager.start.assert_called_with(loop)
    loop.run_until_complete.assert_called_with("check termination condition perodically")

  def test_check_managers(self):
    """
    Test if recovers from failed manager.
    """
    self.test_manager.done = mock.Mock(side_effect = [True, False])
    self.test_manager.should_restart = mock.Mock(return_value = True)
    self.test_manager.start = mock.Mock(return_value = None)
    self.flow.managers = [self.test_manager()]
    self.flow.handler = SyncEventHandler()

    self.flow.loop.run_until_complete(self.flow.check_managers())
    self.assertTrue(1, len(self.flow.managers))
    self.test_manager.start.assert_called_with(self.flow.loop)

  def test_no_restart(self):
    """
    Test if manager with run_always set to false is ignored.
    """
    manager = self.test_manager()
    manager.should_restart = mock.Mock(return_value = False)
    manager.done = mock.Mock(return_value = True)

    self.flow.managers = [manager]

    self.flow.loop.run_until_complete(self.flow.check_managers())
    self.assertFalse(self.flow.managers)

  def test_handle_exceptions(self):
    config_mock = mock.Mock()
    config_mock.FLOWS = ['test']
    config_mock.RAVEN_DSN = None
    self.flow = Flow(config_mock)
    self.flow.running = True

    self.flow.logger.info = mock.Mock()
    run_loop(self.flow.loop)

    args = self.flow.logger.info.call_args

    self.assertTrue(args)

    self.assertEqual(args[1]['extra']['info'][0], ZeroDivisionError)
    self.assertTrue(isinstance(args[1]['extra']['info'][1], ZeroDivisionError))

  def test_raven_capture(self):
    config_mock = mock.Mock()
    config_mock.FLOWS = ['test']
    config_mock.RAVEN_DSN = None
    self.flow = Flow(config_mock)
    self.flow.running = True

    self.flow.raven = mock.Mock()
    self.flow.raven.captureException = mock.Mock()

    run_loop(self.flow.loop)

    self.assertTrue(self.flow.raven.captureException.called)
