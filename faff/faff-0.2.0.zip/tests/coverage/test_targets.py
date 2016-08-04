#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from faff import targets
from faff.include import Include
from faff.variable import Variable
from faff.run import Run
from ..test_case import FaffTestCase


class TestTargets(FaffTestCase):

    def test_coverage(self):
        # Include rules from input file.
        Include(os.path.join(self.get_cwd(), "coverage", "input_test.py"))

        # Test target comparison to none.
        t1 = targets.Target()
        self.assertTrue(t1 < None)

        # Test target optional arguments.
        t2 = targets.Target(args=42)
        self.assertEqual(t2.arguments(), 42)

        # Test target comparison.
        self.assertTrue(t1 < t2)

        # Test rule target comparison to none.
        t3 = targets.RuleTarget(Include.get_rule("rule1"))
        self.assertFalse(t3 < None)

        # Test rule string method.
        str(t3)

        # Test rule target causing error.
        t4 = targets.RuleTarget(Include.get_rule("rule2"))
        with self.assertRaises(Exception):
            self.assertTrue(t4 < None)

        # Test rule target comparison.
        with self.assertRaises(Exception):
            self.assertFalse(t3 < t4)

        # Test file target comparison to none.
        t5 = targets.FileTarget(self.get_cwd(), "coverage", "test_targets.py")
        self.assertFalse(t5 < None)

        # Test file target comparison to self.
        self.assertFalse(t5 < t5)

        # Test file target dirname method.
        self.assertEqual(
            os.path.join(self.get_cwd(), "coverage"), t5.dirname()
        )

        # Test file target without extension.
        # TODO: Test if this is portable.
        Run("rm -rf coverage/tmp/tmp.txt", self.get_cwd())
        t6 = targets.FileTarget(self.get_cwd(), "coverage", "tmp", "tmp.txt")
        self.assertTrue(t6 < None)

        # Test file target copy method.
        t5.copy(self.get_cwd(), "coverage", "tmp", "tmp.txt")
        self.assertFalse(t6 < None)

        # Test file extension replacement.
        t7 = targets.FileTarget(
            self.get_cwd(), "coverage", "test_targets.py", ext=".txt"
        )
        self.assertTrue(t7 < None)

        # Test file target .extension() method.
        self.assertEqual(t7.extension(), ".txt")
        self.assertEqual(t7.extension(True), ".py")

    def test_target_less_than(self):
        # Test target classes less than comparison.
        # Fixed issues with unexpected comparison behaviour.
        # Test base target returns true compared to none.
        # The base .updated() method returns sentinel value of zero which
        # indicates target is out of date regardless of any dependencies.
        t1, t2 = targets.Target(), targets.Target()
        self.assertTrue(t1 < None)

        # Test base target returns true compared to base target.
        # Sentinel value takes precedence over comparison.
        self.assertTrue(t1 < t2)

        # Test updated rule target returns false compared to none.
        # Rule which does not return sentinel value is considered up to date.
        r1, r3 = Include.get_rule("rule1"), Include.get_rule("rule3")
        t2, t3 = targets.RuleTarget(r1), targets.RuleTarget(r3)
        self.assertFalse(t2 < None)

        # Test unsuccessful rule target returns true compared to none.
        # Rule that returns sentinal value is considered out of date.
        self.assertTrue(t3 < None)

        # # Test updated rule compared to unsuccessful rule target returns false.
        # # Test unsuccessful rule compared to updated rule target returns true.
        # self.assertFalse(t2 < t3)
        # self.assertTrue(t3 < t2)

        # Test existing file target compared to none returns false.
        # A file target that exists is considered up to date.
        t4 = targets.FileTarget(self.get_cwd(), "coverage", "test_targets.py")
        self.assertFalse(t4 < None)

        # Test unknown file target compared to none returns true.
        # A file target that does not exist is considered out of date.
        t5 = targets.FileTarget(self.get_cwd(), "coverage", "test_unknown.py")
        self.assertTrue(t5 < None)

    def test_file_target_expansion(self):
        # Test FileTarget variable expansion is not 'sticky'.
        # Fixed an issue where expanded variables in file paths did not change
        # with their defined variables.
        # File target path with variable expansion.
        t1 = targets.FileTarget("{NAME}.py")

        # Test known variable expansion.
        Variable("NAME", "foo")
        self.assertEqual(str(t1), "foo.py")

        # Test modified variable expansion.
        Variable("NAME", "bar")
        self.assertEqual(str(t1), "bar.py")
