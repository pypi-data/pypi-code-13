#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import appier
import appier_extras

class AdminController(appier.Controller):

    @appier.route("/admin/easypay.json", "GET")
    @appier.ensure("admin")
    def easypay(self):
        return self.scheduler.easypay.diagnostics()

    @appier.route("/admin/email.json", "GET")
    @appier.ensure("admin")
    def email_test(self, owner = None):
        owner = owner or appier.get_app()
        email = self.field("email", None)
        if not email: raise appier.OperationalError(
            message = "No email defined"
        )
        appier_extras.admin.Base.send_email_g(
            owner,
            "email/test.html.tpl",
            receivers = [email],
            subject = self.to_locale("Shopdesk test email")
        )
        return dict(email = email)

    @appier.route("/admin/shelve", "GET")
    @appier.ensure("admin")
    def export_shelve(self):
        shelve_path = self.scheduler.easypay.path
        shelve_path = os.path.abspath(shelve_path)
        return self.send_path(shelve_path)
