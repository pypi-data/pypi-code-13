import contextlib
import abc


class MailWrapper(object):

    def __init__(self, config):
        self.config = config

    @abc.abstractmethod
    def send_message(self, rendered, *args, **kwargs):
        pass

    @abc.abstractmethod
    @contextlib.contextmanager
    def connect(self):
        pass