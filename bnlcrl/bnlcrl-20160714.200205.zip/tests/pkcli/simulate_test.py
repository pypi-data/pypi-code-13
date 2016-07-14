# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import pytest

def test_1():
    from bnlcrl.pkcli import simulate
    d = simulate.default_command([2], 24000)
    assert [2] == d['cart_ids']
    assert 24000.0 == d['energy']
