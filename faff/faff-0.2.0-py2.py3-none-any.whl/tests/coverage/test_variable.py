#!/usr/bin/env python
# -*- coding: utf-8 -*-
from faff.variable import Variable
from faff.exceptions import UnknownVariableError
from ..test_case import FaffTestCase


class TestVariable(FaffTestCase):

    def test_coverage(self):
        # Test defined variable expansion.
        var1 = Variable("VAR1", "foo")
        var1 += ["baz"]
        var2 = Variable("VAR2", "bar")
        var2 += "baz"

        # Test for expected expansion.
        s = Variable.expand("{VAR1} {VAR2}")
        self.assertEqual(s, "foo baz bar baz")

        # Test undefined variable expansion.
        with self.assertRaises(UnknownVariableError):
            Variable.expand("{VAR404}")

        # Test defined variable get method.
        var2 = Variable.get("VAR1")

        # Test variable instances are equivalent.
        self.assertEqual(var1, var2)

        # Undefined equality comparison.
        self.assertNotEqual(var1, 42)

        # Test undefined variable get method.
        with self.assertRaises(UnknownVariableError):
            Variable.get("VAR404")

        # Test variable save/restore methods.
        # Define variables to be saved.
        Variable("_VAR1", "foo")
        Variable("_VAR2", "bar")

        # Save variable context.
        ctx = Variable.save()

        # Modify variables and test for expected expansion.
        Variable("_VAR1", "baz")
        Variable("_VAR2", "baz")

        s = Variable.expand("{_VAR1} {_VAR2}")
        self.assertEqual(s, "baz baz")

        # Restore variable context.
        Variable.restore(ctx)

        # Test for expected expansion.
        s = Variable.expand("{_VAR1} {_VAR2}")
        self.assertEqual(s, "foo bar")
