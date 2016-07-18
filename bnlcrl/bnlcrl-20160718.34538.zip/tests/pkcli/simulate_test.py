# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

ndigits = 10


def test_crl_simulator1():
    from bnlcrl.pkcli import simulate
    d = simulate.default_command(['2', '4', '6', '7', '8'], 21500, p0=6.52)
    assert round(0.00120167289264, ndigits) == round(d['d'], ndigits)
    assert round(-0.0661303590822, ndigits) == round(d['d_ideal'], ndigits)
    assert round(1.0480597835, ndigits) == round(d['f'], ndigits)
    assert 6.52 == d['p0']
    assert round(1.24879832711, ndigits) == round(d['p1'], ndigits)
    assert round(1.31613035908, ndigits) == round(d['p1_ideal'], ndigits)


def test_crl_simulator2():
    from bnlcrl.pkcli import simulate
    d = simulate.default_command([], 24000)
    assert 0 == d['d']
    assert 0 == d['d_ideal']
    assert 0 == d['f']
    assert 6.2 == d['p0']
    assert 0 == d['p1']
    assert 0 == d['p1_ideal']
