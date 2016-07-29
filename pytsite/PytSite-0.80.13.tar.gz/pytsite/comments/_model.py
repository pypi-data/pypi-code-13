"""Comments Models.
"""
from typing import Tuple as _Tuple
from datetime import datetime as _datetime
from pytsite import auth as _auth, util as _util, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AbstractComment:
    @property
    def uid(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def parent_uid(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def thread_uid(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def body(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def publish_time(self) -> _datetime:
        raise NotImplementedError("Not implemented yet")

    @property
    def status(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def author(self) -> _auth.model.AbstractUser:
        raise NotImplementedError("Not implemented yet")

    def as_jsonable(self) -> dict:
        return {
            'uid': self.uid,
            'parent_uid': self.parent_uid,
            'thread_uid': self.thread_uid,
            'body': self.body,
            'status': self.body,
            'publish_time': {
                'w3c': _util.w3c_datetime_str(self.publish_time),
                'pretty': _lang.pretty_date_time(self.publish_time),
                'ago': _lang.time_ago(self.publish_time),
            },
            'author': {
                'uid': self.author.uid,
                'nickname': self.author.nickname,
                'full_name': self.author.full_name,
                'picture_url': self.author.picture.get_url(width=50, height=50),
            },
        }
