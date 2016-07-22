import unittest
import os.path as osp
from lxml import etree
import odtlib
from odtlib import fix

HERE = osp.join(osp.dirname(odtlib.__file__), 'test')
DATA = osp.join(HERE, 'data')

CHAR_TRANSLATIONS = [ {'OpenSymbol' : {u'\uf044': u'\ue0ad', u'\uf047': u'\ue0ac', u'\uf046': u'\ue0b4',
                                       u'\uf04a': u'\ue0d0', u'\uf04c': u'\ue0af', u'\uf051': u'\ue0ae',
                                       u'\uf050': u'\ue0b1', u'\uf053': u'\ue0b2', u'\uf057': u'\ue0b6',
                                       u'\uf056': u'\ue0d3', u'\uf059': u'\ue0b5', u'\uf058': u'\ue0b0',
                                       u'\uf061': u'\ue0b7', u'\uf063': u'\ue0cc', u'\uf062': u'\ue0b8',
                                       u'\uf065': u'\ue0cf', u'\uf064': u'\ue0ba', u'\uf067': u'\ue0b9',
                                       u'\uf066': u'\ue0cb', u'\uf069': u'\ue0bf', u'\uf068': u'\ue0bd',
                                       u'\uf06b': u'\ue0c0', u'\uf06a': u'\ue0d4', u'\uf06d': u'\ue0c2',
                                       u'\uf06c': u'\ue0c1', u'\uf06f': u'\ue0c5', u'\uf06e': u'\ue0c3',
                                       u'\uf071': u'\ue0be', u'\uf070': u'\ue0c6', u'\uf073': u'\ue0c8',
                                       u'\uf072': u'\ue0c7', u'\uf075': u'\ue0ca', u'\uf074': u'\ue0c9',
                                       u'\uf077': u'\ue0ce', u'\uf076': u'\ue0d1', u'\uf079': u'\ue0cd',
                                       u'\uf078': u'\ue0c4', u'\uf07a': u'\ue0bc'}} ]

CHARFONT_TRANSLATIONS = [ (('OpenSymbol', 'Courier New'),
                           {u'\uf0a8' : u'\u2666',
                            u'\uf0e0' : u'\u25ca'}) ]

class TestTextFontReplace(unittest.TestCase):

    def test_fix(self):
        tree = etree.parse(osp.join(DATA, 'orig.xml')).getroot()
        params = {'Symbol' : 'OpenSymbol'}
        odtlib.fix.apply_fonts_substitutions(tree, params, CHAR_TRANSLATIONS)
        for fontmap, charmap in CHARFONT_TRANSLATIONS:
            odtlib.fix.update_text_and_fonts(tree, charmap, dict([fontmap]))
        self.assertTextEquals(etree.tostring(tree, pretty_print=True),
                              open(osp.join(DATA, 'fixed.xml')).read())

if __name__ == '__main__':
    unittest.main()
