#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from faff.ext import ChangeLog
from ..test_case import FaffTestCase


class TestChangeLog(FaffTestCase):

    def test_coverage(self):
        ChangeLog(os.path.join(self.get_cwd(), "coverage", "tmp"))
