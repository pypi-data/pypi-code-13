observer = None


# def observer_creator():
#     global observer
#     if observer is None:
#         observer = Observer()
#     return observer


# class Observer(object):
#     def __init__(self):
#         self._observer = []
#         self._observer_length = 0
#
#     def attach_observer(self, obj):
#         self._observer = obj
#         self._observer_length = len(obj)
#
#     def detach_observer(self):
#         self._observer = None
#
#     def notify(self):
#         if self._observer_length != len(self._observer):
#             self.update(self._observer[-1])
#
#     def update(self, data):
#         pass


class Observer(object):
    def __init__(self):
        self._observer = None

    def attach_observer(self, obj):
        self._observer = obj

    def detach_observer(self):
        self._observer = None

    def notify(self, data):
        if self._observer is not None:
            self._observer.update(data)
