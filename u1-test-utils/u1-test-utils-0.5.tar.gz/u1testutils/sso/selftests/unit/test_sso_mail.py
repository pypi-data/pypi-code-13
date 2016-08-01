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

import email.parser
import unittest

import mock

from u1testutils.sso import mail

EMAIL_TEMPLATE = """Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Subject: Ubuntu Single Sign On: Finish your registration
From: Ubuntu Single Sign On <noreply@ubuntu.com>
To: to@example.com

Hello

As a final step of the Ubuntu Single Sign On (SSO) account creation process=
, please validate the email address to@example.com. Ubuntu SSO enables conv=
enient access to a variety of Ubuntu-related services like Ubuntu One with =
the same username and password.

Here is your confirmation code:

%(confirm)s

Enter this code into the registration form, or click the following link to =
automatically confirm your account:

https://login.ubuntu.com/confirm-account/%(confirm)s/to@example.com

If you don\'t know what this is about, then someone has probably entered you=
r email address by mistake. Sorry about that.
If you wish to report this email being incorrectly used, please click the f=
ollowing link:

https://login.ubuntu.com/invalidate-email/%(inval)s/to@example.com

You can also seek further assistance on:

https://forms.canonical.com/sso-support/

Thank you,

The Ubuntu Single Sign On team
https://login.ubuntu.com/
"""


class SSOMailTestCase(unittest.TestCase):

    verification_email = email.parser.Parser().parsestr(
        EMAIL_TEMPLATE % {'confirm': 'QM9CSR', 'inval': '42FcJG'}
    )
    verification_email_long_token = email.parser.Parser().parsestr(
        EMAIL_TEMPLATE % {'confirm': 'dgfjL4kYvTgnCGkBh32n',
                          'inval': 'y74Yh6jkT6Wj89jRgDYy'}
    )

    urls = [
        r'/%s/+new_account',
        r'/invalidate-email/%s/a@b.com',
        r'/confirm-account/%s/a@b.com',
        r'/token/%s/+resetpassword/a@b.com',
        r'/token/%s/+newemail/a@b.com',
    ]

    def setUp(self):
        super(SSOMailTestCase, self).setUp()
        patcher = mock.patch('u1testutils.mail')
        self.mock_mail = patcher.start()
        self.addCleanup(patcher.stop)

    def test_get_verification_code(self):
        self.mock_mail.get_latest_email_sent_to.return_value = \
            self.verification_email
        verification_code = mail.get_verification_code_for_address(
            'to@example.com')
        self.assertEquals(verification_code, 'QM9CSR')

    def test_get_verification_code_long_token(self):
        self.mock_mail.get_latest_email_sent_to.return_value = \
            self.verification_email_long_token
        verification_code = mail.get_verification_code_for_address(
            'to@example.com')
        self.assertEquals(verification_code, 'dgfjL4kYvTgnCGkBh32n')

    def test_get_verification_link(self):
        self.mock_mail.get_latest_email_sent_to.return_value = \
            self.verification_email
        verification_link = mail.get_verification_link_for_address(
            'to@example.com')
        self.assertEquals(
            verification_link,
            'https://login.ubuntu.com/confirm-account/QM9CSR/to@example.com')

    def test_get_verification_link_long_token(self):
        self.mock_mail.get_latest_email_sent_to.return_value = \
            self.verification_email_long_token
        verification_link = mail.get_verification_link_for_address(
            'to@example.com')
        self.assertEquals(
            verification_link,
            'https://login.ubuntu.com/confirm-account/'
            'dgfjL4kYvTgnCGkBh32n/to@example.com')

    def test_get_invalidation_link(self):
        self.mock_mail.get_latest_email_sent_to.return_value = \
            self.verification_email
        invalidation_link = mail.get_invalidation_link_for_address(
            'to@example.com')
        self.assertEquals(
            invalidation_link,
            'https://login.ubuntu.com/invalidate-email/42FcJG/to@example.com')

    def test_get_invalidation_link_long_token(self):
        self.mock_mail.get_latest_email_sent_to.return_value = \
            self.verification_email_long_token
        invalidation_link = mail.get_invalidation_link_for_address(
            'to@example.com')
        self.assertEquals(
            invalidation_link,
            'https://login.ubuntu.com/invalidate-email/'
            'y74Yh6jkT6Wj89jRgDYy/to@example.com')

    def test_no_code(self):
        mock_email = mock.MagicMock()
        mock_email.get_payload.return_value = 'XXXXXX'
        self.mock_mail.get_latest_email_sent_to.return_value = mock_email
        with self.assertRaises(AssertionError):
            mail.get_verification_code_for_address('to@example.com')

    def test_token_regex(self):
        token = 'T0Kenz'
        for pattern in self.urls:
            for host in ('http://localhost:8000', 'https://login.ubuntu.com'):
                url = host + pattern % token
                m = mail.TOKEN_REGEX.search(url)
                self.assertEqual(m.group(1), token)

    def test_token_regex_long(self):
        token = 'dgfjL4kYvTgnCGkBh32n'
        for pattern in self.urls:
            for host in ('http://localhost:8000', 'https://login.ubuntu.com'):
                url = host + pattern % token
                m = mail.TOKEN_REGEX.search(url)
                self.assertEqual(m.group(1), token)

    def test_token_regex_long_bad(self):
        # 0 is not a valid long-token character
        token = 'dgfjL4kYvTgnCGk0h32n'
        for pattern in self.urls:
            for host in ('http://localhost:8000', 'https://login.ubuntu.com'):
                url = host + pattern % token
                m = mail.TOKEN_REGEX.search(url)
                self.assertIsNone(m)
