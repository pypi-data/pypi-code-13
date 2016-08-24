import collections


__version__ = "6.0.0"


class Emitter:
    # special events
    ERROR = object()
    ATTACH = object()
    DETACH = object()

    def __init__(self):
        self._events = {}

    def on(self, event, listener):
        # sanitize arguments types and values

        if event is None:
            raise ValueError("event cannot be None")

        if not callable(listener):
            raise TypeError("listener must be callable")

        # if the event doesn't exists yet, initialize it
        if event not in self._events:
            self._events[event] = collections.OrderedDict()

        # add listener to the event
        self._events[event].update({listener: {"once": False}})

        # emit attach event
        self.emit(Emitter.ATTACH, event, listener)

        return True

    def once(self, event, listener):
        # register the listener through the standard method
        result = self.on(event, listener)

        if not result:
            return result

        # update the "once" setting of the listener to True
        self._events[event].update({listener: {"once": True}})

        return True

    def off(self, event=None, listener=None):
        # if no event given, remove all events
        if event is None:
            # emit detach event for all the listener of all the events
            for event in self._events:
                for listener in self._events[event]:
                    self.emit(Emitter.DETACH, event, listener)

            # delete all events after detach event has been sent
            self._events = {}
            return True

        # if user tries to remove an non-existent event
        if self._events.get(event) is None:
            return False

        # delete all listeners for the given event
        if listener is None:
            # emit a detach event for all the listeners of the given event
            for listener in self._events[event]:
                self.emit(Emitter.DETACH, event, listener)

            # delete all listeners after detach event has been sent
            del self._events[event]
            return True

        # if user tries to remove a non-existent listener
        if self._events[event].get(listener) is None:
            return False

        # emit a detach event
        self.emit(Emitter.DETACH, event, listener)

        # delete the listener after detach event has been sent
        del self._events[event][listener]

        # if no more listeners in the given event, delete it
        if len(self._events[event]) == 0:
            del self._events[event]

        return True

    def events(self):
        # return a new set, containing events
        return set(self._events.keys())

    def listeners(self, event):
        # return a new list, containing listeners of the given event
        return list(self._events.get(event, []))

    def emit(self, event, *args, **kwargs):
        # if user tries to emit the None event
        if event is None:
            return False

        # if user tries to emits a non-existent event
        if self._events.get(event) is None:
            return False

        # trigger each listener attached to the event
        # we iterate on a copy to be allowed to mutate the OrderedDict during
        # iteration
        for listener in list(self._events[event]):
            # trigger the current listener
            try:
                listener(*args, **kwargs)
            except Exception as err:
                # if exception has been raised by error handler, re-raise it
                if event is Emitter.ERROR:
                    raise err

                # emit the error event
                self.emit(Emitter.ERROR, err, *args, **kwargs)
            finally:
                #  if emitter was "once", remove it
                if self._events[event][listener]["once"]:
                    self.off(event, listener)

        return True
