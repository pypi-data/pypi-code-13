#pylint: disable=E0401
"""
Test flow controller.
"""
from unittest import mock
from unittest import TestCase

from aiopype import SyncProtocol
from aiopype.manager import Manager, DescriptiveManager


class TestManager(TestCase):
  def test_get_source(self):
    manager = Manager()
    manager.source = "Test"

    source = manager.get_source()

    self.assertEqual("Test", source)

  def test_done(self):
    manager = Manager()
    manager.source = mock.Mock()
    manager.source.is_done = mock.Mock(return_value = False)

    self.assertFalse(manager.done())

    manager.source.is_done = mock.Mock(return_value = True)

    self.assertTrue(manager.done())

  def test_restart(self):
    manager = Manager()
    manager.run_always = False

    self.assertFalse(manager.should_restart())

    manager.run_always = True

    self.assertTrue(manager.should_restart())

  @mock.patch('aiopype.manager.asyncio')
  def test_start(self, asyncio_mock):
    asyncio_mock.ensure_future = mock.Mock()
    manager = Manager()
    manager.source = mock.Mock()

    manager.source.start = mock.Mock(return_value = 'Test')
    loop = 'loop'

    manager.start(loop)

    asyncio_mock.ensure_future.assert_called_with('Test', loop = 'loop')


class TestDescriptiveManager(TestCase):
  @mock.patch('aiopype.manager.ProcessorRegistry')
  def test_init(self, registry_mock):
    mocksource = mock.MagicMock()
    registry_mock.REGISTRY = {
      'mocksource': mocksource
    }

    class MockDescriptiveManager(DescriptiveManager):
      name = 'mockmanager'
      processors = {
        'source' : {
          'cls': 'mocksource',
          'args': ['a', 'b'],
          'kwargs': {'c' : 1}
        }
      }
      flows = [
        {
          'event': 'mockevent',
          'function': 'test',
          'origin': 'source',
          'target': 'source',
        }
      ]
    handler = SyncProtocol()
    mock_manager = MockDescriptiveManager(handler = handler)

    self.assertTrue(mock_manager.source)
    mocksource.assert_called_with('mockmanager.source', handler, 'a', 'b', c = 1)
    mock_manager.source.on.assert_called_with('mockevent', mock_manager.source.test)
