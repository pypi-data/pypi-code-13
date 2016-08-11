#! /usr/env/bin python
# -*- coding: utf-8 -*-


class A:
    """Test class A."""
    def __init__(self):
        self.x = 5
        self.touch = None


class B:
    """Test class B."""
    def __init__(self):
        self.x = 5
        self.touch = None


def eq_attr(parent_inst, parent_attr, child_inst, child_attr):
    """Set attributes from different class to the same value."""
    child_inst.__dict__[child_attr] = parent_inst.__dict__[parent_attr]
    child_inst.touch = parent_inst.__class__
