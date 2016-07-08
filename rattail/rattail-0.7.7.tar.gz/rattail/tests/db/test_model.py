# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from unittest import TestCase
from mock import patch, DEFAULT, Mock, MagicMock

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from rattail.db import model
from rattail.db.types import GPCType
from rattail.db.changes import record_changes
from rattail.tests import DataTestCase


class SAErrorHelper(object):

    def integrity_or_flush_error(self):
        try:
            from sqlalchemy.exc import FlushError
        except ImportError:
            return IntegrityError
        else:
            return (IntegrityError, FlushError)


class TestPerson(DataTestCase):

    def test_default_display_name_is_generated_from_first_and_last_name_if_both_provided(self):
        person = model.Person(first_name='Fred', last_name='Flintstone')
        self.assertTrue(person.display_name is None)
        self.session.add(person)
        self.session.flush()
        self.assertEqual(person.display_name, 'Fred Flintstone')

    def test_default_display_name_is_generated_from_first_name_if_no_last_name_provided(self):
        person = model.Person(first_name='Fred')
        self.assertTrue(person.display_name is None)
        self.session.add(person)
        self.session.flush()
        self.assertEqual(person.display_name, 'Fred')

    def test_default_display_name_is_generated_from_last_name_if_no_first_name_provided(self):
        person = model.Person(last_name='Flintstone')
        self.assertTrue(person.display_name is None)
        self.session.add(person)
        self.session.flush()
        self.assertEqual(person.display_name, 'Flintstone')


class TestBatch(TestCase):

    # @patch('rattail.db.model.object_session')
    # def test_rowclass(self, object_session):
    #     object_session.return_value = object_session

    #     # no row classes to start with
    #     self.assertEqual(model.Batch._rowclasses, {})

    #     # basic, empty row class
    #     batch = model.Batch(uuid='some_uuid')
    #     batch.get_sqlalchemy_type = Mock(return_value='some_type')
    #     batch.columns = MagicMock()
    #     rowclass = batch.rowclass
    #     self.assertTrue(issubclass(rowclass, model.BatchRow))
    #     self.assertEqual(model.Batch._rowclasses.keys(), ['some_uuid'])
    #     self.assertTrue(model.Batch._rowclasses['some_uuid'] is rowclass)
    #     self.assertFalse(object_session.flush.called)

    #     # make sure rowclass.batch works
    #     object_session.query.return_value.get.return_value = batch
    #     self.assertTrue(rowclass().batch is batch)
    #     object_session.query.return_value.get.assert_called_once_with('some_uuid')

    #     # row class with generated uuid and some columns
    #     batch = model.Batch(uuid=None)
    #     batch.columns = [model.BatchColumn(name='F01'), model.BatchColumn(name='F02')]
    #     model.Batch.get_sqlalchemy_type = Mock(return_value=String(length=20))
    #     def set_uuid():
    #         batch.uuid = 'fresh_uuid'
    #     object_session.flush.side_effect = set_uuid
    #     rowclass = batch.rowclass
    #     object_session.flush.assert_called_once_with()
    #     self.assertEqual(sorted(model.Batch._rowclasses.keys()), sorted(['some_uuid', 'fresh_uuid']))
    #     self.assertTrue(model.Batch._rowclasses['fresh_uuid'] is rowclass)

    def test_get_sqlalchemy_type(self):

        # gpc
        self.assertTrue(isinstance(model.Batch.get_sqlalchemy_type('GPC(14)'), GPCType))

        # boolean
        self.assertTrue(isinstance(model.Batch.get_sqlalchemy_type('FLAG(1)'), sa.Boolean))

        # string
        type_ = model.Batch.get_sqlalchemy_type('CHAR(20)')
        self.assertTrue(isinstance(type_, sa.String))
        self.assertEqual(type_.length, 20)

        # numeric
        type_ = model.Batch.get_sqlalchemy_type('NUMBER(9,3)')
        self.assertTrue(isinstance(type_, sa.Numeric))
        self.assertEqual(type_.precision, 9)
        self.assertEqual(type_.scale, 3)

        # invalid
        self.assertRaises(AssertionError, model.Batch.get_sqlalchemy_type, 'CHAR(9,3)')
        self.assertRaises(AssertionError, model.Batch.get_sqlalchemy_type, 'OMGWTFBBQ')


class TestCustomerPerson(DataTestCase, SAErrorHelper):

    def test_repr(self):
        assoc = model.CustomerPerson(uuid='whatever')
        self.assertEqual(repr(assoc), "CustomerPerson(uuid=u'whatever')")

    def test_customer_required(self):
        assoc = model.CustomerPerson(person=model.Person())
        self.session.add(assoc)
        self.assertRaises(self.integrity_or_flush_error(), self.session.commit)
        self.session.rollback()
        self.assertEqual(self.session.query(model.CustomerPerson).count(), 0)
        assoc.customer = model.Customer()
        self.session.add(assoc)
        self.session.commit()
        self.assertEqual(self.session.query(model.CustomerPerson).count(), 1)

    def test_person_required(self):
        assoc = model.CustomerPerson(customer=model.Customer())
        self.session.add(assoc)
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.assertEqual(self.session.query(model.CustomerPerson).count(), 0)
        assoc.person = model.Person()
        self.session.add(assoc)
        self.session.commit()
        self.assertEqual(self.session.query(model.CustomerPerson).count(), 1)

    def test_ordinal_autoincrement(self):
        customer = model.Customer()
        self.session.add(customer)
        assoc = model.CustomerPerson(person=model.Person())
        customer._people.append(assoc)
        self.session.commit()
        self.assertEqual(assoc.ordinal, 1)
        assoc = model.CustomerPerson(person=model.Person())
        customer._people.append(assoc)
        self.session.commit()
        self.assertEqual(assoc.ordinal, 2)


class TestCustomerGroupAssignment(DataTestCase, SAErrorHelper):

    def test_repr(self):
        assignment = model.CustomerGroupAssignment(uuid='whatever')
        self.assertEqual(repr(assignment), "CustomerGroupAssignment(uuid=u'whatever')")

    def test_customer_required(self):
        assignment = model.CustomerGroupAssignment(group=model.CustomerGroup())
        self.session.add(assignment)
        self.assertRaises(self.integrity_or_flush_error(), self.session.commit)
        self.session.rollback()
        self.assertEqual(self.session.query(model.CustomerGroupAssignment).count(), 0)
        assignment.customer = model.Customer()
        self.session.add(assignment)
        self.session.commit()
        self.assertEqual(self.session.query(model.CustomerGroupAssignment).count(), 1)

    def test_group_required(self):
        assignment = model.CustomerGroupAssignment(customer=model.Customer())
        self.session.add(assignment)
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.assertEqual(self.session.query(model.CustomerGroupAssignment).count(), 0)
        assignment.group = model.CustomerGroup()
        self.session.add(assignment)
        self.session.commit()
        self.assertEqual(self.session.query(model.CustomerGroupAssignment).count(), 1)

    def test_ordinal_autoincrement(self):
        customer = model.Customer()
        self.session.add(customer)
        assignment = model.CustomerGroupAssignment(group=model.CustomerGroup())
        customer._groups.append(assignment)
        self.session.commit()
        self.assertEqual(assignment.ordinal, 1)
        assignment = model.CustomerGroupAssignment(group=model.CustomerGroup())
        customer._groups.append(assignment)
        self.session.commit()
        self.assertEqual(assignment.ordinal, 2)


# class TestCustomerEmailAddress(DataTestCase):

#     def test_pop(self):
#         customer = model.Customer()
#         customer.add_email_address('fred.home@mailinator.com')
#         customer.add_email_address('fred.work@mailinator.com')
#         self.session.add(customer)
#         self.session.commit()
#         self.assertEqual(self.session.query(model.Customer).count(), 1)
#         self.assertEqual(self.session.query(model.CustomerEmailAddress).count(), 2)

#         while customer.emails:
#             customer.emails.pop()
#         self.session.commit()
#         self.assertEqual(self.session.query(model.Customer).count(), 1)
#         self.assertEqual(self.session.query(model.CustomerEmailAddress).count(), 0)

#         # changes weren't being recorded
#         self.assertEqual(self.session.query(model.Change).count(), 0)

#     def test_pop_with_changes(self):
#         record_changes(self.session)

#         customer = model.Customer()
#         customer.add_email_address('fred.home@mailinator.com')
#         customer.add_email_address('fred.work@mailinator.com')
#         self.session.add(customer)
#         self.session.commit()
#         self.assertEqual(self.session.query(model.Customer).count(), 1)
#         self.assertEqual(self.session.query(model.CustomerEmailAddress).count(), 2)

#         while customer.emails:
#             customer.emails.pop()
#         self.session.commit()
#         self.assertEqual(self.session.query(model.Customer).count(), 1)
#         self.assertEqual(self.session.query(model.CustomerEmailAddress).count(), 0)

#         # changes should have been recorded
#         changes = self.session.query(model.Change)
#         self.assertEqual(changes.count(), 3)

#         customer_change = changes.filter_by(class_name='Customer').one()
#         self.assertEqual(customer_change.uuid, customer.uuid)
#         self.assertFalse(customer_change.deleted)

#         email_changes = changes.filter_by(class_name='CustomerEmailAddress')
#         self.assertEqual(email_changes.count(), 2)
#         self.assertEqual([x.deleted for x in email_changes], [True, True])


class TestLabelProfile(DataTestCase):

    def test_get_printer_setting(self):
        profile = model.LabelProfile()
        self.session.add(profile)

        self.assertTrue(profile.uuid is None)
        setting = profile.get_printer_setting('some_setting')
        self.assertTrue(setting is None)
        self.assertTrue(profile.uuid is None)

        profile.uuid = 'some_uuid'
        self.session.add(model.Setting(
                name='labels.some_uuid.printer.some_setting',
                value='some_value'))
        self.session.flush()
        setting = profile.get_printer_setting('some_setting')
        self.assertEquals(setting, 'some_value')

    def test_save_printer_setting(self):
        self.assertEqual(self.session.query(model.Setting).count(), 0)
        profile = model.LabelProfile()
        self.session.add(profile)

        self.assertTrue(profile.uuid is None)
        profile.save_printer_setting('some_setting', 'some_value')
        self.assertFalse(profile.uuid is None)
        self.assertEqual(self.session.query(model.Setting).count(), 1)

        profile.uuid = 'some_uuid'
        profile.save_printer_setting('some_setting', 'some_value')
        self.assertEqual(self.session.query(model.Setting).count(), 2)
        setting = self.session.query(model.Setting)\
            .filter_by(name='labels.some_uuid.printer.some_setting')\
            .one()
        self.assertEqual(setting.value, 'some_value')
