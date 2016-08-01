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

from sst import actions, cases

import u1testutils.sst


class StringPageTestCase(cases.SSTTestCase):

    xserver_headless = True
    base_url = 'file://'
    page_source = (
        """
        <html data-qa-id='test-qa-anchor'>
        </html>
        """
    )

    def setUp(self):
        super(StringPageTestCase, self).setUp()
        self.temp_directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_directory)
        self.page_url_path = os.path.join(self.temp_directory, 'test')

    def test_assert_string_page_is_opened(self):
        page = u1testutils.sst.StringHTMLPage(
            self.page_source, self.page_url_path, qa_anchor='test-qa-anchor',
            open_page=True)
        page.assert_page_is_open()

    def test_string_page_not_opened(self):
        page = u1testutils.sst.StringHTMLPage(
            self.page_source, self.page_url_path, qa_anchor='test-qa-anchor')
        # The page is not opened.
        actions.fails(page.assert_page_is_open)
        # But its file is created.
        with open(self.page_url_path) as page_file:
            page_source = page_file.read()
        self.assertEqual(page_source, self.page_source)
