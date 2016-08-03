
"""

"""
import sys
from tingyun.armoury.ammunition.tracker import current_tracker
from tingyun.armoury.ammunition.external_tracker import wrap_external_trace, parse_parameters
from tingyun.armoury.ammunition.external_tracker import OTHER_ERROR_CODE, ILLEGAL_RESPONSE_ERROR_CODE

try:
    from urllib import ContentTooShortError
except ImportError:
    class ContentTooShortError(Exception):
        pass


def wrap_exception(wrapped, url, parameters, *args, **kwargs):
    """
    """

    tracker = current_tracker()
    if tracker is None:
        return wrapped(*args, **kwargs)

    url = url if not callable(url) else url(*args, **kwargs)
    params = parameters if not callable(parameters) else parameters(*args, **kwargs)

    http_status = 500
    error_code = 0
    params = parse_parameters(url, params)

    try:
        rtv = wrapped(*args, **kwargs)
    except ILLEGAL_RESPONSE_ERROR_CODE:
        error_code = ILLEGAL_RESPONSE_ERROR_CODE
        tracker.record_external_error(url, error_code, http_status, sys.exc_info(), params)
        raise
    except Exception:
        error_code = OTHER_ERROR_CODE
        tracker.record_external_error(url, error_code, http_status, sys.exc_info(), params)
        raise

    try:
        http_status = rtv.getcode()
        if http_status is not None and int(http_status) != 200:
            tracker.record_external_error(url, error_code, int(http_status), sys.exc_info(), params)
    except Exception:
        pass

    return rtv


def detect(module):

    def urllib_url(instance, fullurl, *args, **kwargs):
        return fullurl

    if hasattr(module, 'URLopener'):
        wrap_external_trace(module, 'URLopener.open', 'urllib', urllib_url, exception_wrapper=wrap_exception)
