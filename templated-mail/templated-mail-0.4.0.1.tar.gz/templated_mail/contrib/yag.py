import abc
import contextlib
import sys
from .base import MailWrapper


def patch_argument(cb, kname, default=None, **kwargs):
    return cb(kwargs.get(kname, default))


def patch_arguments(cb, kname, default=None, **kwargs):
    kwargs[kname] = patch_argument(cb, kname, default, **kwargs)
    return kwargs


class YAGMailWrapper(MailWrapper):

    def __init__(self, config):
        super(YAGMailWrapper, self).__init__(config)
        self._yag_config = self._prepare_config(config)
        self._smtp_cls = self._choose_smtp_cls(self._yag_config)

    @staticmethod
    def _choose_smtp_cls(yag_config):
        """
        We assume use of SSL & port 465 if
        the default TLS port, 587, is not
        being used.

        Note that we import yagmail
        here so it isn't a hard requirement
        of templated_mail.
        """

        from yagmail import yagmail
        if int(yag_config['port']) == 587:
            return yagmail.SMTP
        else:
            return yagmail.SMTP_SSL

    def _instantiate_smtp(self):
        return self._smtp_cls(**self._yag_config)

    def _get_connection(self):
        return self._instantiate_smtp()

    @staticmethod
    def _prepare_config(config):
        """
        Create the kind of config yagmail expects
        from the config that templated-mail supports.
        """
        return {
            'host': config.MAIL_HOST,
            'port': config.MAIL_PORT,
            'user': {config.EMAIL_ADDRESS: config.NAME},
            'password': config.EMAIL_PASSWORD,
            'smtp_set_debuglevel': config.DEBUG
        }

    @staticmethod
    def _extra_headers(config, **kwargs):
        return {
            'Reply-To': patch_argument(
                lambda r: r if r is not None else config.REPLY_TO,
                'reply_to', **kwargs
            )
        }

    def send_message(self, rendered, *args, **kwargs):

        with self._get_connection() as conn:

            kwargs = patch_arguments(
                lambda h: h.update(self._extra_headers(self.config, **kwargs)),
                'headers', default={}, **kwargs
            )
            kwargs = patch_arguments(
                lambda p: p if p is not None else self.config.SUPPRESS,
                'preview_only', **kwargs
            )
            conn.send(
                subject=rendered.subject,
                contents=[rendered.html.strip()],
                **kwargs
            )

    @abc.abstractmethod
    def connect(self):
        pass


class YAGmailWithConnecting(YAGMailWrapper):

    def __init__(self, config):
        super(YAGmailWithConnecting, self).__init__(config)
        self._connection = None
        self._keep_connected = False

    @contextlib.contextmanager
    def connect(self):
        """
        This method lets this class be used
        to send multiple emails with the same
        SMTP connection.

        It allows the connection to stay open
        through multiple calls to `send_message`,
        by use of the _keep_connected flag,
        and finally closes the connection itself.

        """
        self._keep_connected = True
        try:
            with self._get_connection():
                yield
        finally:
            self._connection.close()
            self._connection = None
            self._keep_connected = False

    @contextlib.contextmanager
    def _get_connection(self):
        """
        This method allows getting a connection
        which will close at the end of its use
        as a context manager, UNLESS
        self._keep_connected is set, which
        occurs during its use in `connect`.

        """

        exc_info = (exc, exc_type, tb) = (None, None, None)
        context_manager = None
        try:
            if self._connection is None:
                context_manager = self._instantiate_smtp()
                self._connection = context_manager.__enter__()
            yield self._connection

        except Exception:
            exc_info = (exc, exc_type, tb) = sys.exc_info()

        finally:
            if context_manager is not None:
                if not self._keep_connected:
                    context_manager.__exit__(*exc_info)
            if tb is not None:
                del tb


Mail = YAGmailWithConnecting
