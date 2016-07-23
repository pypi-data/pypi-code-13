#-*- coding: utf-8 -*-
import unittest

from kwdensity.density_calculator import DensityCalculator
from kwdensity.tokenizer import Tokenizer
from kwdensity.filters import *


class DensityCalculatorTestCase(unittest.TestCase):

    def setUp(self):
	#  Aristotle
	self.txt = u'''Ζητούμεν λοιπόν να εξετάσωμεν και να μάθωμεν πρώτον την φύσιν και
                   την ουσίαν της ψυχής, έπειτα και πάντα τα συμβεβηκότα και τα
                   φαινόμενα αυτής, από τα οποία άλλα μεν φαίνονται ότι είναι ιδιάζοντα
                   της ψυχής πάθη {1}, άλλα δε ότι υπάρχουσι και εις τα ζώα ένεκα της ψυχής {2}'''
        self.tokenizer = Tokenizer()

    def tearDown(self):
        pass

    def test_init(self):
        calculator = DensityCalculator(tokenizer=self.tokenizer)
        assert isinstance(calculator, DensityCalculator)

    def test_call(self):
        calculator = DensityCalculator(self.tokenizer,
                                       StopwordsFilter('el'))
        densities = calculator(self.txt)
        assert isinstance(densities, list)
        assert len(densities) > 0
        assert densities[0][0] == u'ψυχής'



