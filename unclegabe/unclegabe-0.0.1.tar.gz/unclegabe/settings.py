# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

TEST_RUNNER = 'unclegabe.runners.NoseRunner'
SECRET_KEY = os.environ.get('SECRET_KEY', "foobar")
