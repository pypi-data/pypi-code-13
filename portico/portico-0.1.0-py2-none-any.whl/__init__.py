import traceback
from functools import wraps
from structlog import configure, get_logger
from structlog.processors import JSONRenderer, TimeStamper
from structlog.stdlib import _NAME_TO_LEVEL


def add_log_level(logger, method_name, event_dict):
    event_dict['level'] = _NAME_TO_LEVEL.get(method_name, -1)
    return event_dict


configure(
    processors=[
        add_log_level,
        TimeStamper(fmt='iso', utc=True),
        JSONRenderer(sort_keys=True)
    ],
    context_class=dict
)
log = get_logger()


def wrap_error(raise_error=True, cb=None):
    def wrap(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                trace = traceback.format_exc()
                message = '{}\n{}'.format(e, trace)
                log.error(message)
                if cb:
                    cb(e)
                if raise_error:
                    raise e
        return wrapper
    return wrap
