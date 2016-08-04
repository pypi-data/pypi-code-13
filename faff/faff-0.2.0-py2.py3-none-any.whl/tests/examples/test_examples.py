#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from faff.main import main
from ..test_case import FaffTestCase


class TestExamples(FaffTestCase):

    def test_examples(self):
        examples = (
            ("examples", "gcc_compiler", "faffin01.py"),
            ("examples", "gcc_hello_world", "faffin.py"),
        )
        for example in examples:
            faffin = os.path.join(self.get_cwd(), *example)
            main(["-f", faffin])
