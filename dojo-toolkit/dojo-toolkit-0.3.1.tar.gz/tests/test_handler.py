from unittest import mock

from dojo_toolkit.code_handler import DojoCodeHandler


def test_code_handler():
    notifier = mock.Mock()
    test_runner = mock.Mock()
    code_handler = DojoCodeHandler(notifier=notifier, test_runner=test_runner)
    assert code_handler.notifier == notifier
    assert code_handler.test_runner == test_runner


def test_code_handler_on_modified():
    notifier = mock.Mock()
    test_runner = mock.Mock()
    code_handler = DojoCodeHandler(notifier=notifier, test_runner=test_runner)
    code_handler.on_modified(mock.Mock())
