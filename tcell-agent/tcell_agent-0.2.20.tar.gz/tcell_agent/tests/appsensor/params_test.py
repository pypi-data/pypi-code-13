# coding=utf-8

from __future__ import unicode_literals

import unittest
import re

from tcell_agent.appsensor import params

class ParamsTest(unittest.TestCase):

    def flatten_params_test(self):
        result = params.flatten_clean({
              "action": "index",
              "utf8-char": u"Müller".encode('utf8'),
              "waitlist_entries": {"email": "emailone", "preferences": {"email": "emaildos"}},
              "email_preferences": ["daily_digest", "reminders", u"Müller".encode('utf8')],
              "users": [
                {"email": "one@email.com"},
                {"email": "dos@email.com"},
              ]
            }, None)

        self.assertEqual(result, {
            ("action",): "index",
            ('utf8-char',): "Müller",
            ("waitlist_entries", "email",): "emailone",
            ("waitlist_entries", "preferences", "email",): "emaildos",
            ('0', "email_preferences",): "daily_digest",
            ('1', "email_preferences",): "reminders",
            ('2', 'email_preferences'): "Müller",
            ('0', "users", "email",): "one@email.com",
            ('1', "users", "email",): "dos@email.com"
          })
