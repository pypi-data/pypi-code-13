"""PytSite Comments HTTP API.
"""
from pytsite import auth as _auth
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post_comment(inp: dict) -> dict:
    """Create new comment.
    """
    driver = inp.get('driver')

    thread_uid = inp.get('thread_uid')
    if not thread_uid:
        raise RuntimeError("'thread_uid' is not specified")

    body = inp.get('body')
    if not body:
        raise RuntimeError("'body' is not specified")

    status = 'published'
    parent_uid = inp.get('parent_uid')
    comment = _api.create_comment(thread_uid, body, _auth.current_user(), status, parent_uid, driver)

    return comment.as_jsonable()


def get_comments(inp: dict) -> dict:
    driver = inp.get('driver')

    thread_uid = inp.get('thread_uid')
    if not thread_uid:
        raise RuntimeError("'thread_uid' is not specified")

    limit = int(inp.get('limit', 100))
    if limit > 100:
        limit = 100

    skip = abs(int(inp.get('skip', 0)))
    comments = list(_api.get_driver(driver).get_comments(thread_uid, limit, skip))

    return {
        'remains': _api.get_comments_count(thread_uid, driver) - skip - len(comments),
        'items': [comment.as_jsonable() for comment in comments],
    }
