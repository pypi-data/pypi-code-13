#!/usr/bin/env python
# -*- coding: utf8 -*-

from collections import namedtuple

Event = namedtuple('Event', 'timestamp level ctx function path line_no message tags')