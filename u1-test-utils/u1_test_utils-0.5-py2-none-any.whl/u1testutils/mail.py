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

from __future__ import absolute_import

import imaplib
import time
import uuid
from email import email

from django.conf import settings


def make_unique_test_email_address():
    return settings.EMAIL_ADDRESS_PATTERN % uuid.uuid4()


class MailBox(object):

    def __init__(self, user, password):
        self.user = user
        self.password = password
        if settings.IMAP_USE_SSL:
            self.imap = imaplib.IMAP4_SSL(
                settings.IMAP_SERVER, settings.IMAP_PORT)
        else:
            self.imap = imaplib.IMAP4(
                settings.IMAP_SERVER, settings.IMAP_PORT)

    def __enter__(self):
        self.login()
        return self

    def login(self):
        self.imap.login(self.user, self.password)

    def __exit__(self, type, value, traceback):
        self.close_and_logout()

    def close_and_logout(self):
        self.imap.close()
        self.imap.logout()

    def get_count(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        if data[0] is None:
            return 0
        else:
            return sum(1 for num in data[0].split())

    def fetch_message(self, num):
        self.imap.select('Inbox')
        status, data = self.imap.fetch(str(num), '(RFC822)')
        if data[0] is None:
            raise MailBoxError(
                'There is no message with number {0}'.format(num))
        else:
            email_msg = email.message_from_string(data[0][1])
            return email_msg

    def delete_message(self, num):
        self.imap.select('Inbox')
        self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()

    def delete_all(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        if data[0] is not None:
            for num in data[0].split():
                self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()

    def print_msgs(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        for num in reversed(data[0].split()):
            status, data = self.imap.fetch(num, '(RFC822)')
            print 'Message %s\n%s\n' % (num, data[0][1])

    def get_latest_email_sent_to(self, email_address, timeout=300, poll=1):
        start_time = time.time()
        while ((time.time() - start_time) < timeout):
            # It's no use continuing until we've successfully selected
            # the inbox. And if we don't select it on each iteration
            # before searching, we get intermittent failures.
            status, data = self.imap.select('Inbox')
            if status != 'OK':
                time.sleep(poll)
                continue

            status, data = self.imap.search(None, 'TO', email_address)
            data = [d for d in data if d is not None]
            if status == 'OK' and data:
                for num in reversed(data[0].split()):
                    status, data = self.imap.fetch(num, '(RFC822)')
                    email_msg = email.message_from_string(data[0][1])
                    return email_msg
            time.sleep(poll)

        raise MailBoxError(
            "No email sent to '%s' found in inbox after polling for %s "
            "seconds." % (email_address, timeout))

    def delete_msgs_sent_to(self, email_address):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'TO', email_address)
        message_numbers = data[0]
        if status == 'OK' and message_numbers is not None:
            for num in reversed(message_numbers.split()):
                status, data = self.imap.fetch(num, '(RFC822)')
                self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()


class MailBoxError(Exception):
    """Exception raised on MailBox errors."""


def get_latest_email_sent_to(email_address, timeout=300, poll=1):
    with MailBox(settings.IMAP_USERNAME, settings.IMAP_PASSWORD) as mbox:
        email_msg = mbox.get_latest_email_sent_to(email_address, timeout, poll)
        mbox.delete_msgs_sent_to(email_address)
        return email_msg


def delete_msgs_sent_to(email_address):
    with MailBox(settings.IMAP_USERNAME, settings.IMAP_PASSWORD) as mbox:
        mbox.delete_msgs_sent_to(email_address)


def email_subject_includes(email_msg, text):
    assert text in email_msg['subject'], "'%s' was not in email subject."


def email_body_includes(email_msg, text):
    assert text in email_msg.get_payload(), "'%s' was not in email body."
