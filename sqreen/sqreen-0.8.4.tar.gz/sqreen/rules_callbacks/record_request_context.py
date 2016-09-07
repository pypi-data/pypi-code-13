# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Record request context
"""

from ..rules import RuleCallback
from ..runtime_infos import runtime
from ..frameworks.wsgi import WSGIRequest


class RecordRequestContext(RuleCallback):

    @staticmethod
    def pre(original, *args, **kwargs):
        runtime.store_request(WSGIRequest(args[-2]))

    @staticmethod
    def post(_return, original, *args, **kwargs):
        runtime.clean_request()

    @staticmethod
    def failing(exception, original, *args, **kwargs):
        runtime.clean_request()
