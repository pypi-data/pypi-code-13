# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Record request context
"""
from logging import getLogger
from cgi import escape

from .regexp_rule import RegexpRule
from ..runtime_infos import runtime
from ..utils import is_string

LOGGER = getLogger()


class ReflectedXSSCB(RegexpRule):
    def post(self, _return, original, *args, **kwargs):
        """ Check if a template node returns a content that is in the
        query string
        """
        request = runtime.get_current_request()

        if not request:
            LOGGER.warning("No request was recorded abort")
            return

        if not is_string(_return):
            LOGGER.debug('Non string passed, type %s', type(_return))
            return

        # Get query values
        values = request.query_params_values
        # Check if the return value is present in the values
        match = _return in values
        if match:
            # Check if the value match regexes
            if self.match_regexp(_return):
                # If it is, return the escaped version
                return {'status': 'override', 'new_return_value': self._escape(_return)}
            else:
                print("Do not match regexp")

    def _escape(self, value):
        """ Escape a malicious value to make it safe
        """
        return escape(value, True)
