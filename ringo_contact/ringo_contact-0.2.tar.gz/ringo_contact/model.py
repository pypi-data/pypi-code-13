from sqlalchemy.ext.declarative import declared_attr
import sqlalchemy as sa
from ringo.model import Base
from ringo.model.mixins import Meta, Owned
from ringo.model.base import BaseItem, BaseFactory


class ContactFactory(BaseFactory):

    def create(self, user, values):
        new_item = BaseFactory.create(self, user, values)
        return new_item


class Contact(BaseItem, Meta, Owned, Base):
    """Docstring for contact extension"""

    __tablename__ = 'contacts'
    """Name of the table in the database for this modul. Do not
    change!"""
    _modul_id = None
    """Will be set dynamically. See include me of this modul"""

    # Define columns of the table in the database
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False, default="")
    first_name = sa.Column(sa.String, nullable=False, default="")
    last_name = sa.Column(sa.String, nullable=False, default="")
    organisation = sa.Column(sa.String, nullable=False, default="")
    role = sa.Column(sa.String, nullable=False, default="")
    birtday = sa.Column(sa.Date)
    gender = sa.Column(sa.Integer)

    postalcode = sa.Column(sa.String, nullable=False, default="")
    city = sa.Column(sa.String, nullable=False, default="")
    street = sa.Column(sa.String, nullable=False, default="")

    phone = sa.Column(sa.String, nullable=False, default="")
    fax = sa.Column(sa.String, nullable=False, default="")
    email = sa.Column(sa.String, nullable=False, default="")
    url = sa.Column(sa.String, nullable=False, default="")

    note = sa.Column(sa.Text, nullable=False, default="")

    @classmethod
    def get_item_factory(cls):
        return ContactFactory(cls)


class Contactable(object):
    """Mixin to make items of other modules contactable. This means the
    will get a relation named contacts."""

    @declared_attr
    def contacts(cls):
        clsname = cls.__name__.lower()
        tbl_name = "nm_%s_contacts" % clsname
        nm_table = sa.Table(tbl_name, Base.metadata,
                            sa.Column('%s_id' % clsname, sa.Integer,
                                      sa.ForeignKey(cls.id)),
                            sa.Column('contact_id', sa.Integer,
                                      sa.ForeignKey("contacts.id")))
        contacts = sa.orm.relationship(Contact, secondary=nm_table)
        return contacts
