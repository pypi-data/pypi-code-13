#-*- coding: utf-8 -*-
import unittest

from kwdensity.tokenizer import Tokenizer


class TokenizerTestCase(unittest.TestCase):

    def setUp(self):
	#  Aristotle
	self.txt = u'''Ζητούμεν λοιπόν να εξετάσωμεν και να μάθωμεν πρώτον την φύσιν και
                   την ουσίαν της ψυχής, έπειτα και πάντα τα συμβεβηκότα και τα
                   φαινόμενα αυτής, από τα οποία άλλα μεν φαίνονται ότι είναι ιδιάζοντα
                   της ψυχής πάθη {1}, άλλα δε ότι υπάρχουσι και εις τα ζώα ένεκα της ψυχής {2}'''

    def tearDown(self):
        pass

    def test_init(self):
        tokenizer = Tokenizer()
        assert isinstance(tokenizer, Tokenizer)

    def test_call(self):
	expected = [u'Ζητούμεν', u'λοιπόν', u'να', u'εξετάσωμεν', u'και', u'να',
                    u'μάθωμεν', u'πρώτον', u'την', u'φύσιν', u'και',
                    u'την', u'ουσίαν', u'της', u'ψυχής', u'έπειτα', u'και',
                    u'πάντα', u'τα', u'συμβεβηκότα', u'και', u'τα', u'φαινόμενα',
                    u'αυτής', u'από', u'τα', u'οποία', u'άλλα', u'μεν',
                    u'φαίνονται', u'ότι', u'είναι', u'ιδιάζοντα',
                    u'της', u'ψυχής', u'πάθη', u'1', u'άλλα', u'δε', u'ότι',
                    u'υπάρχουσι', u'και', u'εις', u'τα', u'ζώα', u'ένεκα',
                    u'της', u'ψυχής', u'2',]
        tokenizer = Tokenizer()
        result = tokenizer(text=self.txt)
        assert isinstance(result, list)
        assert len(result) == len(expected)
        assert result == expected



