
from .base import MailWrapper
import contextlib

class SimpleMailWrapper(MailWrapper):

    def __init__(self, config):
        import simple_mail
        super(SimpleMailWrapper, self).__init__(config)
        self._mail = simple_mail.Mail(config)

    def send_message(self, rendered, *args, **kwargs):
        self._mail.send_message(
            rendered.subject,
            *args,
            body=rendered.body,
            html=rendered.html,
            **kwargs
        )

    @contextlib.contextmanager
    def connect(self):
        raise NotImplementedError


Mail = SimpleMailWrapper