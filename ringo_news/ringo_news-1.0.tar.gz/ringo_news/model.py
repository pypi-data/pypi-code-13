import sqlalchemy as sa
from pyramid.security import Allow, Authenticated
from ringo.lib.security import get_permissions
from ringo.model import Base
from ringo.model.base import BaseItem, BaseFactory


nm_news_user = sa.Table(
    'nm_news_user', Base.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('uid', sa.Integer, sa.ForeignKey('users.id')),
    sa.Column('nid', sa.Integer, sa.ForeignKey('news.id'))
)
"""Table to store the unread (visible) news for a user. If the user has read
the news the entry in this table can be removed"""


class NewsFactory(BaseFactory):

    def create(self, user, values):
        new_item = BaseFactory.create(self, user, values)
        return new_item


class News(BaseItem, Base):
    """Docstring for news extension"""

    __tablename__ = 'news'
    """Name of the table in the database for this modul. Do not
    change!"""
    _modul_id = None
    """Will be set dynamically. See include me of this modul"""

    # Define columns of the table in the database
    id = sa.Column(sa.Integer, primary_key=True)

    # Define relations to other tables
    subject = sa.Column(sa.String)
    text = sa.Column(sa.Text)
    date = sa.Column(sa.Date)

    users = sa.orm.relationship("User",
                                secondary=nm_news_user,
                                backref='news')

    @classmethod
    def _get_permissions(cls, modul, item, request):
        """Returns custom privileges for news entries. As News do not
        have an owner nor a group the default permisssion system of
        Ringo would deny all access form users except from users with
        admin role. So we need to overwrite the default persmissions.
        News items should be readable by all authenticated users.

        This means setting permissions on roles does not have any
        effect!"""
        # Default permissions (e.g allow admins access)
        permissions = get_permissions(modul, item)
        # Add custom read permission
        permissions.append((Allow, Authenticated, 'read'))
        return permissions

    @classmethod
    def get_item_factory(cls, request=None):
        return NewsFactory(cls, request)
