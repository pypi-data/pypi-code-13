from unittest import mock

from dojo_toolkit.dojo import Dojo


def test_dojo():
    dojo = Dojo('/foo/bar')
    assert dojo.round_time
    assert dojo.event_handler
    assert dojo.observer
    assert dojo.timer_thread


@mock.patch('dojo_toolkit.dojo.dojo_timer')
@mock.patch('dojo_toolkit.dojo.Observer')
def test_dojo_start(observer, dojo_timer):
    dojo = Dojo('/foo/bar')
    with mock.patch('time.sleep') as sleep:
        sleep.side_effect = KeyboardInterrupt
        dojo.start()
