# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 by the Free Software Foundation, Inc.
#
# This file is part of Django-Mailman.
#
# Django-Mailman is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Django-Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Django-Mailman.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, print_function, unicode_literals

import os

from django.test import RequestFactory
from django.contrib.messages.storage.cookie import CookieStorage


def get_flash_messages(response, empty=True):
    if "messages" not in response.cookies:
        return []
    # A RequestFactory will not run the messages middleware, and thus will
    # not delete the messages after retrieval.
    dummy_request = RequestFactory().get("/")
    dummy_request.COOKIES["messages"] = response.cookies["messages"].value
    msgs = list(CookieStorage(dummy_request))
    if empty:
        del response.client.cookies["messages"]
    return msgs
get_flash_messages.__test__ = False


def get_test_file(*fileparts):
    return os.path.join(os.path.dirname(__file__), "testdata", *fileparts)
get_test_file.__test__ = False
