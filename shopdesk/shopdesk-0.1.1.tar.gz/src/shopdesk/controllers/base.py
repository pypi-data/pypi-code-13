#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class BaseController(appier.Controller):

    @appier.route("/notification", "GET")
    def notification(self):
        cin = self.field("ep_cin")
        username = self.field("ep_user")
        doc = self.field("ep_doc")
        api = self.scheduler.easypay
        result = api.notify_mb(cin, username, doc)
        self.content_type("application/xml")
        return result
