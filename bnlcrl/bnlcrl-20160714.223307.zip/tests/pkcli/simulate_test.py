# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


def test_crl_simulator1():
    from bnlcrl.pkcli import simulate
    d = simulate.default_command([2], 24000, lens_array=(1, 3, 5))
    assert [2] == d['cart_ids']
    assert 24000.0 == d['energy']
    assert (1, 3, 5) == d['lens_array']


def test_crl_simulator2():
    from bnlcrl.pkcli import simulate
    d = simulate.default_command([], 24000)
    assert [] == d['cart_ids']
    assert 24000.0 == d['energy']
    assert (1, 2, 4, 8, 16) == d['lens_array']
