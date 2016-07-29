"""PytSite Comments API.
"""
from typing import Dict as _Dict, Iterable as _Iterable
from frozendict import frozendict as _frozendict
from pytsite import router as _router, widget as _widget, auth as _auth, reg as _reg, lang as _lang, cache as _cache
from . import _driver, _error, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_last_registered_driver_name = None  # type: str
_drivers = {}  # type: _Dict[str, _driver.Abstract]
_comments_count = _cache.create_pool('pytsite.comments.count')
_comment_body_max_length = int(_reg.get('comments.body_max_length', 2048))


def register_driver(driver: _driver.Abstract):
    """Registers a driver.
    """
    global _drivers

    if not isinstance(driver, _driver.Abstract):
        raise TypeError("Instance of 'pytsite.comments.driver.Abstract' expected.")

    driver_name = driver.get_name()

    if driver_name in _drivers:
        raise _error.DriverAlreadyRegistered("Driver '{}' is already registered".format(driver_name))

    _drivers[driver_name] = driver

    global _last_registered_driver_name
    _last_registered_driver_name = driver_name


def get_drivers() -> _frozendict:
    """Returns all registered drivers.
    """
    return _frozendict(_drivers)


def get_comment_statuses() -> dict:
    """Get valid comment statuses.
    """
    return {
        'published': _lang.t('pytsite.comments@status_published'),
        'on_moderation': _lang.t('pytsite.comments@status_on_moderation'),
        'spam': _lang.t('pytsite.comments@status_spam'),
        'deleted': _lang.t('pytsite.comments@status_deleted'),
    }


def get_comment_body_max_length() -> int:
    """Get comment's body maximum length.
    """
    return _comment_body_max_length


def get_driver(driver_name: str = None) -> _driver.Abstract:
    """Get registered driver instance.
    """
    if not driver_name:
        driver_name = _reg.get('comments.default_driver', _last_registered_driver_name)

    if not _driver:
        raise _error.DriverNotRegistered('No comments driver registered.')

    if driver_name not in _drivers:
        raise _error.DriverNotRegistered("Driver '{}' is not registered".format(driver_name))

    return _drivers[driver_name]


def get_widget(widget_uid: str = 'comments', thread_id: str = None, driver: str = None) -> _widget.Abstract:
    """Get comments widget from the driver.
    """
    return get_driver(driver).get_widget(widget_uid, thread_id or _router.current_url())


def create_comment(thread_id: str, body: str, author: _auth.model.AbstractUser, status: str = 'published',
                   parent_uid: str = None, driver_name: str = None) -> _model.AbstractComment:
    """Create new comment.
    """
    if len(body) > _comment_body_max_length:
        raise RuntimeError(_lang.t('pytsite.comments@error_body_too_long'))

    if status not in get_comment_statuses():
        raise _error.InvalidCommentStatus("'{}' is not a valid comment's status.".format(status))

    return get_driver(driver_name).create_comment(thread_id, body, author, status, parent_uid)


def get_comments(driver: str, thread_id: str, limit: int = 100, skip: int = 0, status: str = 'published') \
        -> _Iterable[_model.AbstractComment]:
    """Get comments from driver.
    """
    return get_driver(driver).get_comments(thread_id, limit, skip, status)


def get_comments_count(thread_uid: str, driver: str = None) -> int:
    """Get comments count for thread and driver.
    """
    c_key = '{}_{}'.format(thread_uid, driver)

    if _comments_count.has(c_key):
        return _comments_count.get(c_key)

    count = get_driver(driver).get_comments_count(thread_uid)
    _comments_count.put(c_key, count, 300)

    return count


def get_all_comments_count(thread_id: str):
    """Get comments count for particular thread, all drivers.
    """
    count = 0
    for driver_name in _drivers:
        count += get_comments_count(thread_id, driver_name)

    return count
