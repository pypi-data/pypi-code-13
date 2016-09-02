#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Opbeat API
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Opbeat API.
#
# Hive Opbeat API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Opbeat API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Opbeat API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

BASE_URL = "https://intake.opbeat.com/api/v1/"
""" The default base url to be used when no other
base url value is provided to the constructor """

class Api(appier.Api):

    def __init__(self, *args, **kwargs):
        appier.Api.__init__(self, *args, **kwargs)
        self.app_id = appier.conf("OPBEAT_APP_ID", None)
        self.org_id = appier.conf("OPBEAT_ORG_ID", None)
        self.token = appier.conf("OPBEAT_TOKEN", None)
        self.base_url = kwargs.get("base_url",  BASE_URL)
        self.app_id = kwargs.get("app_id", self.app_id)
        self.org_id = kwargs.get("org_id", self.org_id)
        self.token = kwargs.get("token", self.token)
        self._build_url()

    def build(
        self,
        method,
        url,
        data = None,
        data_j = None,
        data_m = None,
        headers = None,
        params = None,
        mime = None,
        kwargs = None
    ):
        auth = kwargs.pop("auth", True)
        if not auth: return
        headers["Authorization"] = "Bearer %s" % self.token

    def release(self, payload = {}):
        url = self.app_url + "releases/"
        contents = self.post(url, data_j = payload)
        return contents

    def error(self, payload = {}):
        url = self.app_url + "errors/"
        contents = self.post(url, data_j = payload)
        return contents

    def _build_url(self):
        self.app_url = self.base_url + "organizations/%s/apps/%s/" % (self.org_id, self.app_id)
