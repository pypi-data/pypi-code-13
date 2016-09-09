# -*- coding: utf-8 -*-
# Payfort Python bindings
# API docs at https://docs.start.payfort.com/references/api
# Authors:
# Maria Repela <m.repela@bvblogic.com>
# Alex Vorobyov <a.vorobyov@bvblogic.com>

# Configuration variables

__version__ = "0.0.3"

api_key = None
api_base = 'https://api.start.source.com'
api_version = None

from .resource import *
from .errors import *
