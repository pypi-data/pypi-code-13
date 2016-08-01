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
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import tempfile
import uuid

import testscenarios
from sst import cases

import u1testutils.sst
from u1testutils import logging
from u1testutils.sso import (
    data,
    sst as sso_sst,
)


_WRONG_PAGE_SOURCE = (
    """
    <html data-qa-id="wrong">
    </html>
    """
)

_SITE_NOT_RECOGNIZED_PAGE_SOURCE = (
    """
    <html data-qa-id="decide">
      <div data-qa-id="info-items">
        <input type="checkbox"/>
      </div>
      <button data-qa-id="rp_confirm_login" />
    </html>
    """
)

_CREATE_ACCOUNT_FROM_REDIRECT_PAGE_SOURCE = (
    """
    <html data-qa-id="new_account">
      <form data-qa-id="create_account_form"
          action="{create_account_form_submit_link}" method="get" >
        <input id="id_email" type="email" />
        <input id="id_displayname" type="text" />
        <input id="id_password" type="password" />
        <input id="id_passwordconfirm" type="password" />
        <input id="recaptcha_response_field" type="text" />
        <input id="id_accept_tos" type="checkbox" />
        <button data-qa-id="register_button" type="submit" />
      </form>
    </html>
    """
)

_UNIFIED_LOGIN_FROM_REDIRECT_PAGE_SOURCE = (
    """
    <html data-qa-id="login">
      <head>
        <title>Log in</title>
      </head>
      <span data-qa-id="brand_ubuntuone" />
      <form data-qa-id="login_form" action="{login_form_submit_link}"
          method="get" >
        <input id="id_email" type="email" />
        <input id="id_password" type="password" />
        <button data-qa-id="login_button" type="submit">
          Log in
        </button>
      </form>
      <a href="{create_account_link}" data-qa-id="user_intention_create">
        create account
      </a>
    </html>
    """
)


_UNIFIED_CREATE_ACCOUNT_FROM_REDIRECT_PAGE_SOURCE = (
    """
    <html data-qa-id="login">
      <head>
        <title>Log in</title>
      </head>
      <span data-qa-id="brand_ubuntuone" />
      <form data-qa-id="create_account_form"
          action="{create_account_form_submit_link}" method="get" >
        <input id="id_email" type="email" />
        <input id="id_displayname" type="text" />
        <input id="id_password" type="password" />
        <input id="id_passwordconfirm" type="password" />
        <input id="recaptcha_response_field" type="text" />
        <input id="id_accept_tos" type="checkbox" />
        <button data-qa-id="register_button" type="submit" />
      </form>
    </html>
    """
)


class FakeSSOWebsite(object):

    def __init__(self, is_user_logged_in, is_site_recognized, brand):
        super(FakeSSOWebsite, self).__init__()
        self.is_user_logged_in = is_user_logged_in
        self.is_site_recognized = is_site_recognized
        self.brand = brand

    def __enter__(self):
        self.temp_directory = tempfile.mkdtemp()
        self._write_fake_pages()

    def _write_fake_pages(self):
        if self.is_site_recognized:
            not_recognized_path = ''
        else:
            not_recognized_path = self._write_fake_site_not_recognized_page()
        if not self.is_user_logged_in:
            self._write_login_and_create_account_pages(not_recognized_path)

    def _write_fake_site_not_recognized_page(self):
        source = _SITE_NOT_RECOGNIZED_PAGE_SOURCE
        path = '+decide'
        qa_anchor = 'decide'
        return self._write_fake_page_with_token(path, source, qa_anchor)

    def _write_fake_page_with_token(self, path, source, qa_anchor, **links):
        # We do not check the tokens, so the easiest thing is to have the
        # every page in separate paths, to write them to HTML files and be able
        # to open all of them on the same test. In real life, the tokens are
        # the same. To check the token can be a future improvement.
        # -- elopio - 2013-07-03
        token = str(uuid.uuid1())
        token_directory = os.path.join(self.temp_directory, token)
        os.mkdir(token_directory)
        return self._write_fake_page(
            token_directory, path, source, qa_anchor, **links)

    def _write_fake_page(self, directory, path, source, qa_anchor, **links):
        if links:
            source = source.format(**links)
        page_path = os.path.join(directory, path)
        u1testutils.sst.StringHTMLPage(
            source, page_path, qa_anchor, open_page=True)
        return page_path

    def _write_login_and_create_account_pages(self, next_page_path):
        create_account_path = self._write_fake_unified_create_account_page(
            next_page_path)
        self._write_fake_unified_login_page(
            next_page_path, create_account_path)

    def _write_fake_unified_create_account_page(self, next_page_path):
        source = _UNIFIED_CREATE_ACCOUNT_FROM_REDIRECT_PAGE_SOURCE
        path = '+decide'
        qa_anchor = 'login'
        return self._write_fake_page_with_token(
            path, source, qa_anchor,
            create_account_form_submit_link=next_page_path)

    def _write_fake_unified_login_page(
            self, next_page_path, create_account_path):
        source = _UNIFIED_LOGIN_FROM_REDIRECT_PAGE_SOURCE
        path = '+decide'
        qa_anchor = 'login'
        return self._write_fake_page_with_token(
            path, source, qa_anchor,
            login_form_submit_link=next_page_path,
            create_account_link=create_account_path)

    def _write_fake_create_account_page(self, next_page_path):
        source = _CREATE_ACCOUNT_FROM_REDIRECT_PAGE_SOURCE
        path = '+new_account'
        qa_anchor = 'new_account'
        return self._write_fake_page_with_token(
            path, source, qa_anchor,
            create_account_form_submit_link=next_page_path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.temp_directory)


class WrongSSOSiteTestCase(cases.SSTTestCase):

    xserver_headless = True

    def setUp(self):
        self.base_url = 'file://'
        super(WrongSSOSiteTestCase, self).setUp()
        self._write_wrong_page()

    def _write_wrong_page(self):
        temp_directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, temp_directory)
        page_path = os.path.join(temp_directory, 'wrong')
        u1testutils.sst.StringHTMLPage(
            _WRONG_PAGE_SOURCE, page_path, qa_anchor='wrong',
            open_page=True)

    def test_sign_in(self):
        self.assertRaises(
            AssertionError, sso_sst.sign_in, user='not important',
            is_site_recognized=False)

    def test_create_account(self):
        self.assertRaises(
            AssertionError, sso_sst.sign_in, user='not important',
            is_site_recognized=False)


class SignInTestCase(
        testscenarios.TestWithScenarios, cases.SSTTestCase,
        logging.LogHandlerTestCase):

    scenarios = [
        ('ubuntuone brand', {'brand': 'ubuntuone'}),
        ('other brand', {'brand': 'other'}),
    ]

    xserver_headless = True

    def setUp(self):
        self.base_url = 'file://'
        super(SignInTestCase, self).setUp()

    def test_sign_in_with_already_signed_user_to_site_recognized(self):
        # Sign in will do nothing.
        sso_sst.sign_in(user=None, is_site_recognized=True)

    def test_sign_in_with_already_signed_user_to_site_not_recognized(self):
        with FakeSSOWebsite(
                is_user_logged_in=True, is_site_recognized=False,
                brand=self.brand):
            sso_sst.sign_in(user=None, is_site_recognized=False)

    def test_sign_in_to_site_recognized(self):
        user = data.User.make_unique()
        with FakeSSOWebsite(
                is_user_logged_in=False, is_site_recognized=True,
                brand=self.brand):
            sso_sst.sign_in(user, is_site_recognized=True)

    def test_sign_in_to_site_not_recognized(self):
        user = data.User.make_unique()
        with FakeSSOWebsite(
                is_user_logged_in=False, is_site_recognized=False,
                brand=self.brand):
            sso_sst.sign_in(user, is_site_recognized=False)

    def test_sign_in_with_unexpected_site_not_recognized(self):
        user = data.User.make_unique()
        with FakeSSOWebsite(
                is_user_logged_in=False, is_site_recognized=False,
                brand=self.brand):
            self.assertRaises(
                AssertionError, sso_sst.sign_in, user, is_site_recognized=True)
        self.assertLogLevelContains(
            'ERROR',
            'Please check that you are accessing SSO from a server that is '
            'trusted. Otherwise, the unexpected Site Not Recognized page will '
            'be opened.'
        )


class CreateNewAccountTestCase(
        testscenarios.TestWithScenarios, cases.SSTTestCase,
        logging.LogHandlerTestCase):

    scenarios = [
        ('ubuntuone brand', {'brand': 'ubuntuone'}),
        ('other brand', {'brand': 'other'}),
    ]

    xserver_headless = True

    def setUp(self):
        self.temp_directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_directory)
        self.base_url = 'file://' + self.temp_directory
        super(CreateNewAccountTestCase, self).setUp()

    def test_create_account_to_site_recognized(self):
        user = data.User.make_unique()
        with FakeSSOWebsite(
                is_user_logged_in=False, is_site_recognized=True,
                brand=self.brand):
            sso_sst.create_new_account(user, is_site_recognized=True)

    def test_create_account_to_site_not_recognized(self):
        user = data.User.make_unique()
        with FakeSSOWebsite(
                is_user_logged_in=False, is_site_recognized=False,
                brand=self.brand):
            sso_sst.create_new_account(user, is_site_recognized=False)

    def test_create_account_with_unexpected_site_not_recognized(self):
        user = data.User.make_unique()
        with FakeSSOWebsite(
                is_user_logged_in=False, is_site_recognized=False,
                brand=self.brand):
            self.assertRaises(
                AssertionError, sso_sst.create_new_account, user,
                is_site_recognized=True)
        self.assertLogLevelContains(
            'ERROR',
            'Please check that you are accessing SSO from a server that is '
            'trusted. Otherwise, the unexpected Site Not Recognized page will '
            'be opened.'
        )
