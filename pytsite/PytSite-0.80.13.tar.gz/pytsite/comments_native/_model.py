"""Comments Models.
"""
from typing import Tuple as _Tuple
from datetime import datetime as _datetime
from pytsite import odm as _odm, odm_ui as _odm_ui, comments as _comments, image as _image, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Comment(_comments.model.AbstractComment, _odm_ui.model.UIEntity):
    def _setup_fields(self):
        """Setup fields.
        """
        self.define_field(_odm.field.String('thread_uid', nonempty=True))
        self.define_field(_odm.field.String('body', nonempty=True, strip_html=True,
                                            max_length=_comments.get_comment_body_max_length()))
        self.define_field(_odm.field.RefsUniqueList('images', model='images'))
        self.define_field(_odm.field.String('status', nonempty=True, default='published'))
        self.define_field(_odm.field.DateTime('publish_time', nonempty=True, default=_datetime.now()))
        self.define_field(_odm.field.Ref('author', model='user', nonempty=True))

    def _setup_indexes(self):
        """Setup indexes.
        """
        self.define_index([('thread_uid', _odm.I_ASC), ('status', _odm.I_ASC)])
        self.define_index([('publish_time', _odm.I_ASC)])
        self.define_index([('author', _odm.I_ASC)])

    @property
    def uid(self) -> str:
        return str(self.id)

    @property
    def parent_uid(self) -> str:
        return str(self.parent.id) if self.parent else None

    @property
    def thread_uid(self) -> str:
        return self.f_get('thread_uid')

    @property
    def body(self) -> str:
        return self.f_get('body')

    @property
    def publish_time(self) -> _datetime:
        return self.f_get('publish_time')

    @property
    def images(self) -> _Tuple[_image.model.Image]:
        return self.f_get('images')

    @property
    def status(self) -> str:
        return self.f_get('status')

    @property
    def author(self) -> _auth.model.AbstractUser:
        return self.f_get('author')
