#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import unittest
import doctest
import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends, doctest_dropdb
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction


class AccountTestCase(unittest.TestCase):
    'Test Account module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('account')
        self.account_template = POOL.get('account.account.template')
        self.tax_code_template = POOL.get('account.tax.code.template')
        self.tax_template = POOL.get('account.tax.code.template')
        self.account = POOL.get('account.account')
        self.account_create_chart = POOL.get(
            'account.create_chart', type='wizard')
        self.company = POOL.get('company.company')
        self.user = POOL.get('res.user')
        self.fiscalyear = POOL.get('account.fiscalyear')
        self.sequence = POOL.get('ir.sequence')
        self.move = POOL.get('account.move')
        self.journal = POOL.get('account.journal')
        self.account_type = POOL.get('account.account.type')
        self.period = POOL.get('account.period')
        self.balance_non_deferral = POOL.get(
            'account.fiscalyear.balance_non_deferral', type='wizard')
        self.tax = POOL.get('account.tax')

    def test0005views(self):
        'Test views'
        test_view('account')

    def test0006depends(self):
        'Test depends'
        test_depends()

    def test0010account_chart(self):
        'Test creation of minimal chart of accounts'
        with Transaction().start(DB_NAME, USER,
                context=CONTEXT) as transaction:
            account_template, = self.account_template.search([
                    ('parent', '=', None),
                    ])
            tax_account, = self.account_template.search([
                    ('name', '=', 'Main Tax'),
                    ])
            with Transaction().set_user(0):
                tax_code = self.tax_code_template()
                tax_code.name = 'Tax Code'
                tax_code.account = account_template
                tax_code.save()
                base_code = self.tax_code_template()
                base_code.name = 'Base Code'
                base_code.account = account_template
                base_code.save()
                tax = self.tax_template()
                tax.name = tax.description = '20% VAT'
                tax.type = 'percentage'
                tax.rate = Decimal('0.2')
                tax.account = account_template
                tax.invoice_account = tax_account
                tax.credit_note_account = tax_account
                tax.invoice_base_code = base_code
                tax.invoice_base_sign = Decimal(1)
                tax.invoice_tax_code = tax_code
                tax.invoice_tax_sign = Decimal(1)
                tax.credit_note_base_code = base_code
                tax.credit_note_base_sign = Decimal(-1)
                tax.credit_note_tax_code = tax_code
                tax.credit_note_tax_sign = Decimal(-1)
                tax.save()

            company, = self.company.search([
                    ('rec_name', '=', 'Dunder Mifflin'),
                    ])
            self.user.write([self.user(USER)], {
                    'main_company': company.id,
                    'company': company.id,
                    })
            CONTEXT.update(self.user.get_preferences(context_only=True))

            session_id, _, _ = self.account_create_chart.create()
            create_chart = self.account_create_chart(session_id)
            create_chart.account.account_template = account_template
            create_chart.account.company = company
            create_chart.transition_create_account()
            receivable, = self.account.search([
                    ('kind', '=', 'receivable'),
                    ('company', '=', company.id),
                    ])
            payable, = self.account.search([
                    ('kind', '=', 'payable'),
                    ('company', '=', company.id),
                    ])
            create_chart.properties.company = company
            create_chart.properties.account_receivable = receivable
            create_chart.properties.account_payable = payable
            create_chart.transition_create_properties()
            transaction.cursor.commit()

    def test0020fiscalyear(self):
        'Test fiscalyear'
        with Transaction().start(DB_NAME, USER,
                context=CONTEXT) as transaction:
            today = datetime.date.today()
            company, = self.company.search([
                    ('rec_name', '=', 'Dunder Mifflin'),
                    ])
            sequence, = self.sequence.create([{
                        'name': '%s' % today.year,
                        'code': 'account.move',
                        'company': company.id,
                        }])
            fiscalyear, = self.fiscalyear.create([{
                        'name': '%s' % today.year,
                        'start_date': today.replace(month=1, day=1),
                        'end_date': today.replace(month=12, day=31),
                        'company': company.id,
                        'post_move_sequence': sequence.id,
                        }])
            self.fiscalyear.create_period([fiscalyear])
            self.assertEqual(len(fiscalyear.periods), 12)
            transaction.cursor.commit()

    def test0030account_debit_credit(self):
        'Test account debit/credit'
        with Transaction().start(DB_NAME, USER,
                context=CONTEXT) as transaction:
            fiscalyear, = self.fiscalyear.search([])
            period = fiscalyear.periods[0]
            journal_revenue, = self.journal.search([
                    ('code', '=', 'REV'),
                    ])
            journal_expense, = self.journal.search([
                    ('code', '=', 'EXP'),
                    ])
            revenue, = self.account.search([
                    ('kind', '=', 'revenue'),
                    ])
            receivable, = self.account.search([
                    ('kind', '=', 'receivable'),
                    ])
            expense, = self.account.search([
                    ('kind', '=', 'expense'),
                    ])
            payable, = self.account.search([
                    ('kind', '=', 'payable'),
                    ])
            # Create some moves
            vlist = [
                {
                    'period': period.id,
                    'journal': journal_revenue.id,
                    'date': period.start_date,
                    'lines': [
                        ('create', [{
                                    'account': revenue.id,
                                    'credit': Decimal(100),
                                    }, {
                                    'account': receivable.id,
                                    'debit': Decimal(100),
                                    }]),
                        ],
                    },
                {
                    'period': period.id,
                    'journal': journal_expense.id,
                    'date': period.start_date,
                    'lines': [
                        ('create', [{
                                    'account': expense.id,
                                    'debit': Decimal(30),
                                    }, {
                                    'account': payable.id,
                                    'credit': Decimal(30),
                                    }]),
                        ],
                    },
                ]
            self.move.create(vlist)

            # Test debit/credit
            self.assertEqual((revenue.debit, revenue.credit),
                (Decimal(0), Decimal(100)))
            self.assertEqual(revenue.balance, Decimal(-100))

            # Use next fiscalyear
            next_sequence, = self.sequence.create([{
                        'name': 'Next Year',
                        'code': 'account.move',
                        'company': fiscalyear.company.id,
                        }])
            next_fiscalyear, = self.fiscalyear.copy([fiscalyear],
                default={
                    'start_date': fiscalyear.end_date + datetime.timedelta(1),
                    'end_date': fiscalyear.end_date + datetime.timedelta(360),
                    'post_move_sequence': next_sequence.id,
                    'periods': None,
                    })
            self.fiscalyear.create_period([next_fiscalyear])

            # Test debit/credit for next year
            with Transaction().set_context(fiscalyear=next_fiscalyear.id):
                revenue = self.account(revenue.id)
                self.assertEqual((revenue.debit, revenue.credit),
                    (Decimal(0), Decimal(0)))
                self.assertEqual(revenue.balance, Decimal(-100))

            # Test debit/credit cumulate for next year
            with Transaction().set_context(fiscalyear=next_fiscalyear.id,
                    cumulate=True):
                revenue = self.account(revenue.id)
                self.assertEqual((revenue.debit, revenue.credit),
                    (Decimal(0), Decimal(100)))
                self.assertEqual(revenue.balance, Decimal(-100))

            # Balance non-deferral
            journal_sequence, = self.sequence.search([
                    ('code', '=', 'account.journal'),
                    ])
            journal_closing, = self.journal.create([{
                        'name': 'Closing',
                        'code': 'CLO',
                        'type': 'situation',
                        'sequence': journal_sequence.id,
                        }])
            period_closing, = self.period.create([{
                        'name': 'Closing',
                        'start_date': fiscalyear.end_date,
                        'end_date': fiscalyear.end_date,
                        'fiscalyear': fiscalyear.id,
                        'type': 'adjustment',
                        }])
            type_equity, = self.account_type.search([
                    ('name', '=', 'Equity'),
                    ])
            account_pl, = self.account.create([{
                        'name': 'P&L',
                        'type': type_equity.id,
                        'deferral': True,
                        'parent': revenue.parent.id,
                        'kind': 'other',
                        }])

            session_id = self.balance_non_deferral.create()[0]
            balance_non_deferral = self.balance_non_deferral(session_id)

            balance_non_deferral.start.fiscalyear = fiscalyear
            balance_non_deferral.start.journal = journal_closing
            balance_non_deferral.start.period = period_closing
            balance_non_deferral.start.credit_account = account_pl
            balance_non_deferral.start.debit_account = account_pl

            balance_non_deferral._execute('balance')

            moves = self.move.search([
                    ('state', '=', 'draft'),
                    ('period.fiscalyear', '=', fiscalyear.id),
                    ])
            self.move.post(moves)

            # Close fiscalyear
            self.fiscalyear.close([fiscalyear])

            # Check deferral
            self.assertEqual(revenue.deferrals, ())

            deferral_receivable, = receivable.deferrals
            self.assertEqual(
                (deferral_receivable.debit, deferral_receivable.credit),
                (Decimal(100), Decimal(0)))
            self.assertEqual(deferral_receivable.fiscalyear, fiscalyear)

            # Test debit/credit
            with Transaction().set_context(fiscalyear=fiscalyear.id):
                revenue = self.account(revenue.id)
                self.assertEqual((revenue.debit, revenue.credit),
                    (Decimal(100), Decimal(100)))
                self.assertEqual(revenue.balance, Decimal(0))

                receivable = self.account(receivable.id)
                self.assertEqual((receivable.debit, receivable.credit),
                    (Decimal(100), Decimal(0)))
                self.assertEqual(receivable.balance, Decimal(100))

            # Test debit/credit for next year
            with Transaction().set_context(fiscalyear=next_fiscalyear.id):
                revenue = self.account(revenue.id)
                self.assertEqual((revenue.debit, revenue.credit),
                    (Decimal(0), Decimal(0)))
                self.assertEqual(revenue.balance, Decimal(0))

                receivable = self.account(receivable.id)
                self.assertEqual((receivable.debit, receivable.credit),
                    (Decimal(0), Decimal(0)))
                self.assertEqual(receivable.balance, Decimal(100))

            # Test debit/credit cumulate for next year
            with Transaction().set_context(fiscalyear=next_fiscalyear.id,
                    cumulate=True):
                revenue = self.account(revenue.id)
                self.assertEqual((revenue.debit, revenue.credit),
                    (Decimal(0), Decimal(0)))
                self.assertEqual(revenue.balance, Decimal(0))

                receivable = self.account(receivable.id)
                self.assertEqual((receivable.debit, receivable.credit),
                    (Decimal(100), Decimal(0)))
                self.assertEqual(receivable.balance, Decimal(100))

            transaction.cursor.rollback()

    def test0040tax_compute(self):
        'Test tax compute'
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            today = datetime.date.today()

            tax_account, = self.account.search([
                    ('name', '=', 'Main Tax'),
                    ])
            tax = self.tax()
            tax.name = tax.description = 'Test'
            tax.type = 'none'
            tax.invoice_account = tax_account
            tax.credit_note_account = tax_account

            child1 = self.tax()
            child1.name = child1.description = 'Child 1'
            child1.type = 'percentage'
            child1.rate = Decimal('0.2')
            child1.invoice_account = tax_account
            child1.credit_note_account = tax_account
            child1.save()

            child2 = self.tax()
            child2.name = child2.description = 'Child 1'
            child2.type = 'fixed'
            child2.amount = Decimal('10')
            child2.invoice_account = tax_account
            child2.credit_note_account = tax_account
            child2.save()

            tax.childs = [child1, child2]
            tax.save()

            self.assertEqual(self.tax.compute([tax], Decimal('100'), 2),
                [{
                        'base': Decimal('200'),
                        'amount': Decimal('40.0'),
                        'tax': child1,
                        }, {
                        'base': Decimal('200'),
                        'amount': Decimal('20'),
                        'tax': child2,
                        }])

            child1.end_date = today + relativedelta(days=5)
            child1.save()
            self.assertEqual(self.tax.compute([tax], Decimal('100'), 2, today),
                [{
                        'base': Decimal('200'),
                        'amount': Decimal('40.0'),
                        'tax': child1,
                        }, {
                        'base': Decimal('200'),
                        'amount': Decimal('20'),
                        'tax': child2,
                        }])

            child1.start_date = today + relativedelta(days=1)
            child1.save()
            self.assertEqual(self.tax.compute([tax], Decimal('100'), 2, today),
                [{
                        'base': Decimal('200'),
                        'amount': Decimal('20'),
                        'tax': child2,
                        }])
            self.assertEqual(self.tax.compute([tax], Decimal('100'), 2,
                    today + relativedelta(days=1)), [{
                        'base': Decimal('200'),
                        'amount': Decimal('40.0'),
                        'tax': child1,
                        }, {
                        'base': Decimal('200'),
                        'amount': Decimal('20'),
                        'tax': child2,
                        }])
            self.assertEqual(self.tax.compute([tax], Decimal('100'), 2,
                    today + relativedelta(days=5)), [{
                        'base': Decimal('200'),
                        'amount': Decimal('40.0'),
                        'tax': child1,
                        }, {
                        'base': Decimal('200'),
                        'amount': Decimal('20'),
                        'tax': child2,
                        }])
            self.assertEqual(self.tax.compute([tax], Decimal('100'), 2,
                    today + relativedelta(days=6)), [{
                        'base': Decimal('200'),
                        'amount': Decimal('20'),
                        'tax': child2,
                        }])

            child1.end_date = None
            child1.save()
            self.assertEqual(self.tax.compute([tax], Decimal('100'), 2,
                    today + relativedelta(days=6)), [{
                        'base': Decimal('200'),
                        'amount': Decimal('40.0'),
                        'tax': child1,
                        }, {
                        'base': Decimal('200'),
                        'amount': Decimal('20'),
                        'tax': child2,
                        }])


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite:
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountTestCase))
    suite.addTests(doctest.DocFileSuite(
            'scenario_account_reconciliation.rst',
            setUp=doctest_dropdb, tearDown=doctest_dropdb, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
