import pytest
from emitter import Emitter


# testing the special events:
# Emitter.ATTACH
# Emitter.DETACH
# Emitter.ERROR


# Emitter.ATTACH


def test_attach__1():
    """
    ATTACH listeners are triggered on their own registration.
    """
    emitter = Emitter()
    l = []

    def attach_listener(event, listener):
        l.append(1)

    emitter.on(Emitter.ATTACH, attach_listener)

    assert len(l) == 1


def test_attach__2():
    """
    ATTACH listeners get the event and the listener that have been registered.
    """
    emitter = Emitter()
    d = {}

    # ATTACH callback receives the event and the listener
    def attach_listener(event, listener):
        d["event"] = event
        d["listener"] = listener

    emitter.on(Emitter.ATTACH, attach_listener)
    emitter.on("event", callable)

    assert d["event"] == "event"
    assert d["listener"] == callable


def test_attach__3():
    """
    ATTACH event is triggered even on listeners updates.
    """
    emitter = Emitter()
    l = []

    emitter.on(Emitter.ATTACH, lambda event, listener: l.append(1))

    emitter.on("event", callable)
    emitter.on("event", callable)

    assert len(l) == 3


# Emitter.DETACH


def test_detach__1():
    """
    DETACH event is triggered when removing a listener.
    """
    emitter = Emitter()
    l = []

    emitter.on(Emitter.DETACH, lambda err, *args, **kwargs: l.append(1))
    emitter.on("event", callable)

    emitter.off("event", callable)

    assert len(l) == 1


def test_detach__2():
    """
    DETACH event is not triggered if listener does not exists.
    """
    emitter = Emitter()
    l = []

    emitter.on(Emitter.DETACH, lambda err, *args, **kwargs: l.append(1))

    emitter.off("event", callable)

    assert len(l) == 0


def test_detach__3():
    """
    DETACH event is triggered for each listener when removing a whole event.
    """
    emitter = Emitter()
    l = []

    emitter.on(Emitter.DETACH, lambda err, *args, **kwargs: l.append(1))

    emitter.on("event", callable)
    emitter.on("event", bool)

    emitter.off("event")

    assert len(l) == 2


def test_detach__4():
    """
    DETACH is triggered for each listener of each event.
    """
    emitter = Emitter()
    l = []

    emitter.on(Emitter.DETACH, lambda err, *args, **kwargs: l.append(1))

    emitter.on("event1", callable)
    emitter.on("event1", bool)
    emitter.on("event2", callable)
    emitter.on("event2", bool)

    emitter.off()

    assert len(l) == 5


def test_detach__5():
    """
    DETACH listener receives the event and the listener affected.
    """
    emitter = Emitter()
    d = {}

    def detach_listener(event, listener):
        d["event"] = event
        d["listener"] = listener

    emitter.on(Emitter.DETACH, detach_listener)
    emitter.on("event", callable)

    emitter.off("event", callable)

    assert d["event"] == "event"
    assert d["listener"] == callable


# Emitter.ERROR


def test_error__1():
    """
    ERROR event is emitted when listener raises exception.
    """
    emitter = Emitter()
    l = []

    def listener(*args, **kwargs):
        raise Exception()

    emitter.on("thing", listener)
    emitter.on(Emitter.ERROR, lambda err: l.append(1))

    emitter.emit("thing")
    assert len(l) == 1


def test_error__2():
    """
    ERROR event handler gets error, *args and **kwargs.
    """
    emitter = Emitter()
    d = {}

    def listener(*args, **kwargs):
        raise Exception()

    def handler(err, *args, **kwargs):
        d["err"] = err
        d["args"] = args
        d["kwargs"] = kwargs

    emitter.on("thing", listener)
    emitter.on(Emitter.ERROR, handler)

    emitter.emit("thing", 10, b=20)

    assert isinstance(d["err"], Exception)
    assert d["args"][0] == 10
    assert d["kwargs"]["b"] == 20


def test_error__3():
    """
    If ERROR event handler raises exception, it is re-raised, and Emitter
    does not emit the ERROR event.
    """
    emitter = Emitter()
    l = []

    def listener(*args, **kwargs):
        raise Exception()

    def handler(err, *args, **kwargs):
        l.append(1)
        raise StopIteration()

    emitter.on(Emitter.ERROR, handler)
    emitter.on("event", listener)

    with pytest.raises(StopIteration):
        emitter.emit("event")

    assert len(l) == 1


def test_error__4():
    """
    One time ERROR listener is removed even if it raises exception.
    """
    emitter = Emitter()
    l = []

    def listener(*args, **kwargs):
        raise Exception()

    def handler(err, *args, **kwargs):
        l.append(1)
        raise StopIteration()

    emitter.once(Emitter.ERROR, handler)
    emitter.on("event", listener)

    assert len(emitter.listeners(Emitter.ERROR)) == 1

    with pytest.raises(StopIteration):
        emitter.emit("event")

    assert len(emitter.listeners(Emitter.ERROR)) == 0


