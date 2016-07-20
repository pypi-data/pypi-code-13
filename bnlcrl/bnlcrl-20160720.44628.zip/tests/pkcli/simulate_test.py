# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from bnlcrl.pkcli import simulate

ndigits = 10
verbose = False


def test_crl_simulator1():
    d = simulate.simulate_crl(['2', '4', '6', '7', '8'], 21500, p0=6.52, verbose=verbose)
    assert round(0.00120167289264, ndigits) == round(d['d'], ndigits)
    assert round(-0.0661303590822, ndigits) == round(d['d_ideal'], ndigits)
    assert round(1.0480597835, ndigits) == round(d['f'], ndigits)
    assert 6.52 == d['p0']
    assert round(1.24879832711, ndigits) == round(d['p1'], ndigits)
    assert round(1.31613035908, ndigits) == round(d['p1_ideal'], ndigits)


def test_crl_simulator1a():
    d = simulate.simulate_crl(['2', '4', '6', '7', '8'], 21500, p0=6.52, verbose=verbose, use_numpy=True)
    assert round(0.00120167289264, ndigits) == round(d['d'], ndigits)
    assert round(-0.0661303590822, ndigits) == round(d['d_ideal'], ndigits)
    assert round(1.0480597835, ndigits) == round(d['f'], ndigits)
    assert 6.52 == d['p0']
    assert round(1.24879832711, ndigits) == round(d['p1'], ndigits)
    assert round(1.31613035908, ndigits) == round(d['p1_ideal'], ndigits)


def test_crl_simulator2():
    d = simulate.simulate_crl([], 24000)
    assert 0 == d['d']
    assert 0 == d['d_ideal']
    assert 0 == d['f']
    assert 6.2 == d['p0']
    assert 0 == d['p1']
    assert 0 == d['p1_ideal']


# TODO: add tests for different data formats (csv, json, plain text)

def test_delta_finder1():
    d = simulate.find_delta(24000, precise=True, data_file='Be_delta.dat', verbose=verbose)
    assert 5.91145636e-07 == d['characteristic_value']
    assert 24001.0234 == d['closest_energy']


def test_delta_finder1a():
    d = simulate.find_delta(24000, precise=True, data_file='Be_delta.dat', verbose=verbose, use_numpy=True)
    assert 5.91145636e-07 == d['characteristic_value']
    assert 24001.0234 == d['closest_energy']


def test_delta_finder2():
    d = simulate.find_delta(24000, precise=True, data_file='', verbose=verbose)
    assert 5.91196169e-07 == d['characteristic_value']
    assert 23999.998 == d['closest_energy']


def test_delta_finder3():
    d = simulate.find_delta(24000, calc_delta=True, verbose=verbose)
    assert 5.908635405401086e-07 == d['characteristic_value']
    assert 24000 == d['closest_energy']


def test_atten_finder2():
    d = simulate.find_delta(10000, precise=True, data_file='', characteristic='atten', verbose=verbose)
    assert 9594.11 == d['characteristic_value']
    assert 10000.0 == d['closest_energy']
