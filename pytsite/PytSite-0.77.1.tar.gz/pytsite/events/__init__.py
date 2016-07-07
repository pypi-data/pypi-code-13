"""Event Subsystem.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_listeners = {}


def listen(event: str, listener: callable, call_once: bool = False, priority: int = 0):
    """Add an event listener.
    """
    global _listeners
    if event not in _listeners:
        _listeners[event] = []

    _listeners[event].append((listener, call_once, priority))

    # Sort listeners by priority
    _listeners[event] = sorted(_listeners[event], key=lambda x: x[2])


def fire(event: str, stop_after: int = None, **kwargs):
    """Fires an event to listeners.
    """
    if event not in _listeners:
        return

    count = 0
    for handler, call_once, priority in _listeners[event]:
        handler(**kwargs)
        count += 1
        if stop_after and count >= stop_after:
            break

    # Remove handlers which should be called once
    _listeners[event] = [item for item in _listeners[event] if not item[1]]


def first(event: str, **kwargs):
    """Fires an event and process only one handler.
    """
    return fire(event, stop_after=1, **kwargs)
