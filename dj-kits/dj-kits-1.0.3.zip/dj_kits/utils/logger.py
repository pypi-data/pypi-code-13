# -*- coding: utf-8 -*-
import logging
from functools import partial

ddt = logging.getLogger('ddt')

debug = partial(ddt.debug)
info = partial(ddt.info)
warning = partial(ddt.warning)
error = partial(ddt.error)
critical = partial(ddt.critical)
