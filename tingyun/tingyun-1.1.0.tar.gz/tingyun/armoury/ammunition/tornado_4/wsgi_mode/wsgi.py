
"""define module for tornado wsgi entrance. but not support tornado core functions

"""

from tingyun.armoury.trigger.wsgi_entrance import wsgi_application_wrapper


def detect_wsgi_entrance(module):
    """
    :param module:
    :return:
    """
    try:
        import tornado
        version = tornado.version
    except Exception:
        version = "xx"

    wsgi_application_wrapper(module.WSGIAdapter, '__call__', ('Tornado', version))
