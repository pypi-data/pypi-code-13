# coding: utf-8
# !/usr/bin/python

"""
Project: simulator
Wed Jul 20 21:17:18 2016
"""

from simulator.models import Resistor, ResistorInSeries
import pytest

# Author
__author__ = 'Jason Xing Zhang'
__email__ = 'xingz@uvic.ca'

def test_resistor():
    """
    test parameters 
    """
    resistor = Resistor.Resistor(23)
    assert resistor(i=10) == 230

def test_resistor_in_series():
    """
    test solver
    """
    resistor_in_series = ResistorInSeries.ResistorInSeries(23, 37)
    resistor_in_series.states_probe('r1')
    results = []
    for i in range(10):
        results.append(resistor_in_series(i=i, logger=True))
    assert results == [0, 60, 120, 180, 240, 300, 360, 420, 480, 540]
    assert resistor_in_series.probe_results == {'r1': [{'outputs': 0},
                                                       {'outputs': 23},
                                                       {'outputs': 46},
                                                       {'outputs': 69},
                                                       {'outputs': 92},
                                                       {'outputs': 115},
                                                       {'outputs': 138},
                                                       {'outputs': 161},
                                                       {'outputs': 184},
                                                       {'outputs': 207}
                                                      ]
                                               }
