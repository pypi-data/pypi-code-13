#!/usr/bin/env python
# -*- coding: utf-8 -*-
import faff
import subprocess


@faff.Option("-o", "--option", type=str)
def option1(opt):
    """Example option."""
    pass


@faff.rule()
def rule1(target, depends, args):
    """Example rule without targets/dependencies."""
    pass


@faff.rule(options=option1)
def rule2(target, depends, args):
    """Example rule which raises an unknown error."""
    raise Exception("unknown error")


@faff.rule()
def rule3(target, depends, args):
    """Example rule which raises a subprocess error."""
    raise subprocess.CalledProcessError(1, "unknown", "subprocess error")
