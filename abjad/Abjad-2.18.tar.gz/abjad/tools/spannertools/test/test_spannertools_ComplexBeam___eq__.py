# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_ComplexBeam___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.ComplexBeam()
    spanner_2 = spannertools.ComplexBeam()

    assert not spanner_1 == spanner_2
