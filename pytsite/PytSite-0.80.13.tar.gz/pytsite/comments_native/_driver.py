"""PytSite Comments Abstract Driver.
"""
from typing import Iterable as _Iterable
from pytsite import widget as _widget, auth as _auth, comments as _comments, odm as _odm
from . import _model
from ._widget import Comments as _CommentsWidget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Native(_comments.driver.Abstract):
    """Abstract Comments Driver.
    """

    def get_name(self) -> str:
        """Get driver name.
        """
        return 'native'

    def create_comment(self, thread_uid: str, body: str, author: _auth.model.AbstractUser, status: str = 'published',
                       parent_uid: str = None) -> _comments.model.AbstractComment:
        """Create new comment.
        """
        e = _odm.dispense('comment')
        e.f_set('thread_uid', thread_uid)
        e.f_set('body', body)
        e.f_set('author', author)
        e.f_set('status', status)
        e.f_set('_parent', _odm.get_by_ref('comment:' + parent_uid)) if parent_uid else None
        e.save()

        return e

    def get_widget(self, widget_uid: str, thread_id: str) -> _widget.Abstract:
        """Get comments widget for particular thread.
        """
        return _CommentsWidget(widget_uid, thread_id=thread_id)

    def get_comments(self, thread_uid: str, limit: int = 100, skip: int = 0, status: str = 'published') \
            -> _Iterable[_comments.model.AbstractComment]:
        """Get comments.
        """
        f = _odm.find('comment').where('thread_uid', '=', thread_uid).where('status', '=', status)
        return f.sort([('publish_time', _odm.I_ASC)]).skip(skip).get(limit)

    def get_comments_count(self, thread_uid: str) -> int:
        """Get comments count for particular thread.
        """
        return _odm.find('comment').where('thread_uid', '=', thread_uid).where('status', '=', 'published').count()
