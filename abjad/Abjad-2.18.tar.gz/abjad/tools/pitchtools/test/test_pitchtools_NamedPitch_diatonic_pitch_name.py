# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch_diatonic_pitch_name_01():

    assert NamedPitch("cs''").diatonic_pitch_name == "c''"
