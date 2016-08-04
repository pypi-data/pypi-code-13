#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from faff import targets
from faff.rule import rule
from faff.include import Include
from faff.exceptions import (
    InvalidTargetError,
    InvalidOptionError,
)
from ..test_case import FaffTestCase


class TestRule(FaffTestCase):

    def test_coverage(self):
        # Include rules from input file.
        Include(os.path.join(self.get_cwd(), "coverage", "input_test.py"))

        # Create a rule target.
        rule_target1 = targets.RuleTarget(Include.get_rule("rule1"))

        # Test rule definition with keyword arguments.
        @rule(
            depends=rule_target1,
            options=Include.get_option("option1"),
        )
        def irule3(target, depends, args):
            pass

        # Test rule call method.
        irule3()

        # # Test invalid keyword arguments raise exceptions.
        # with self.assertRaises(InvalidTargetError):
        #     @rule(
        #         depends=None,
        #         options=Include.get_option("option1"),
        #     )
        #     def rule4(target, depends, args):
        #         pass
        #
        # with self.assertRaises(InvalidOptionError):
        #     @rule(
        #         depends=rule_target1,
        #         options=None,
        #     )
        #     def rule5(target, depends, args):
        #         pass

        # Test rule pattern 2.
        @rule(rule_target1)
        def rule6(target, depends, args):
            pass

        # Test rule pattern 3
        @rule([rule_target1, rule_target1])
        def rule7(target, depends, args):
            pass
