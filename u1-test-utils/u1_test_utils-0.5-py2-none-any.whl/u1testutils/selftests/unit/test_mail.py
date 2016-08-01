# -*- coding: utf-8 -*-

# Copyright 2013 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License version 3, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/

import socket
import threading
import time
import unittest
from email.mime import text as mime_text

import localmail
import localmail.tests.helpers
from django.conf import settings

from u1testutils import mail


SMTP_PORT = 2025

localmail_thread = None


def setUpModule():
    global localmail_thread
    localmail_thread = threading.Thread(
        target=localmail.run, args=(SMTP_PORT, settings.IMAP_PORT))
    # Avoid hanging the main process when something goes wrong
    localmail_thread.daemon = True
    localmail_thread.start()
    # There is a race here as there is no (easy, that I know of) way to
    # guarantee that the server has reached the point that it is listening
    # to the socket. This leads to conection errors in these cases.  So the
    # workaround is to... sleep :-/ The proper way to handle this would be
    # to add an Event() in the server that can be waited on in the client
    # (or any other sync mechanism including making sure run() blocks until
    # the listen calls have been really executed) -- vila 2013-05-22
    time.sleep(0.1)
    # Try the port to make sure the server started.
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_.settimeout(10)
    socket_.connect(('localhost', SMTP_PORT))
    socket_.close()


def tearDownModule():
    global localmail_thread
    localmail.shutdown_thread(localmail_thread)


def _send_email(body, subject, from_, to):
    message = mime_text.MIMEText(body)
    message['Subject'] = subject
    message['From'] = from_
    message['To'] = to
    with localmail.tests.helpers.SMTPClient(port=SMTP_PORT) as smtp:
        smtp.send(message)


class MailBoxTestCase(unittest.TestCase):

    def setUp(self):
        super(MailBoxTestCase, self).setUp()
        self.mail_box = mail.MailBox(
            settings.IMAP_USERNAME, settings.IMAP_PASSWORD)
        self.mail_box.login()
        self.addCleanup(self._clean_mail_box)

    def _clean_mail_box(self):
        self.mail_box.delete_all()
        self.mail_box.close_and_logout()

    def test_get_count_with_empty_inbox(self):
        self.assertEqual(self.mail_box.get_count(), 0)

    def test_get_count_with_messages_received(self):
        for i in xrange(3):
            _send_email(
                'Test body', 'Test Subject', 'from@example.com',
                'to@example.com')
        self.assertEqual(self.mail_box.get_count(), 3)

    def test_fetch_email(self):
        _send_email(
            'Test body', 'Test Subject', 'from@example.com', 'to@example.com')
        email = self.mail_box.fetch_message(1)
        self.assertEquals(email.get_payload(), 'Test body' + '\n')

    def test_fetch_email_with_wrong_number(self):
        with self.assertRaises(mail.MailBoxError) as error:
            self.mail_box.fetch_message(1)
        self.assertEqual(
            error.exception.message, 'There is no message with number 1')

    def test_delete_message(self):
        _send_email(
            'Test message to delete', 'Test Subject', 'from@example.com',
            'to@example.com')
        _send_email(
            'Test message to keep', 'Test Subject', 'from@example.com',
            'to@example.com')
        self.mail_box.delete_message(1)
        self.assertEqual(self.mail_box.get_count(), 1)
        email = self.mail_box.fetch_message(1)
        self.assertEquals(email.get_payload(), 'Test message to keep' + '\n')

    def test_delete_all_with_no_messages(self):
        self.mail_box.delete_all()
        self.assertEqual(self.mail_box.get_count(), 0)

    def test_delete_all_with_messages(self):
        for i in xrange(3):
            _send_email(
                'Test body', 'Test Subject', 'from@example.com',
                'to@example.com')
        self.mail_box.delete_all()
        self.assertEqual(self.mail_box.get_count(), 0)

    def test_get_latest_email_sent_to_address_with_no_messages(self):
        with self.assertRaises(mail.MailBoxError) as error:
            self.mail_box.get_latest_email_sent_to('test@example.com', 1)
        self.assertEqual(
            error.exception.message,
            "No email sent to 'test@example.com' found in inbox after polling "
            "for 1 seconds.")

    def test_get_latest_email_sent_to_address(self):
        _send_email(
            'Test message to somebody else', 'Test Subject',
            'from@example.com', 'someone-else@example.com')
        body = 'Test message to me'
        subject = 'Test Subject to me'
        from_ = 'from-me@example.com'
        to = 'to-me@example.com'
        _send_email(body, subject, from_, to)
        latest_email = self.mail_box.get_latest_email_sent_to('me@example.com')
        self.assertEquals(latest_email['From'], from_)
        self.assertEquals(latest_email['To'], to)
        self.assertEquals(latest_email['Subject'], subject)
        self.assertEquals(
            latest_email.get_payload(), body + '\n')

    def test_delete_messages_sent_to_address_with_no_messages(self):
        # Test for bug #1199098.
        # It should not throw an exception.
        self.mail_box.delete_msgs_sent_to('i-have-no-messages@example.com')

    def test_delete_messages_sent_to_address(self):
        body = 'Test message to somebody else'
        subject = 'Test Subject to somebody else'
        from_ = 'from@example.com'
        to = 'someone-else@example.com'
        _send_email(body, subject, from_, to)
        _send_email(
            'Test message to me', 'Test Subject', 'from@example.com',
            'me@example.com')
        self.mail_box.delete_msgs_sent_to('me@example.com')
        self.assertEqual(self.mail_box.get_count(), 1)
        # Assert that the other mail remains in the inbox.
        latest_email = self.mail_box.get_latest_email_sent_to(
            'someone-else@example.com')
        self.assertEquals(latest_email['From'], from_)
        self.assertEquals(latest_email['To'], to)
        self.assertEquals(latest_email['Subject'], subject)
        self.assertEquals(
            latest_email.get_payload(), body + '\n')


class MailHelpersTestCase(unittest.TestCase):

    def test_get_latest_email(self):
        _send_email(
            'Test body', 'Test Subject', 'from@example.com',
            'to@example.com')
        latest_email = mail.get_latest_email_sent_to('to@example.com')
        self.assertEquals(
            latest_email.get_payload(), 'Test body' + '\n')
        # Assert that the email was deleted.
        self._assert_messages_count(0)

    def _assert_messages_count(self, expected_number):
        with mail.MailBox(
                settings.IMAP_USERNAME, settings.IMAP_PASSWORD) as mbox:
            self.assertEqual(mbox.get_count(), expected_number)

    def test_delete_messages_sent_to_email(self):
        _send_email(
            'Test body', 'Test Subject', 'from@example.com', 'to@example.com')
        self._assert_messages_count(1)
        mail.delete_msgs_sent_to('to@example.com')
        self._assert_messages_count(0)
