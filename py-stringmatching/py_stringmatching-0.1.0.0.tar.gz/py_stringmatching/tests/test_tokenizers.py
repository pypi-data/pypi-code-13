from __future__ import unicode_literals

import unittest
from nose.tools import *

from py_stringmatching.tokenizer.alphabetic_tokenizer import AlphabeticTokenizer
from py_stringmatching.tokenizer.alphanumeric_tokenizer import AlphanumericTokenizer
from py_stringmatching.tokenizer.delimiter_tokenizer import DelimiterTokenizer
from py_stringmatching.tokenizer.qgram_tokenizer import QgramTokenizer
from py_stringmatching.tokenizer.whitespace_tokenizer import WhitespaceTokenizer


class QgramTokenizerTestCases(unittest.TestCase):
    def setUp(self):
        self.qg1_tok = QgramTokenizer(1)
        self.qg2_tok = QgramTokenizer()
        self.qg2_tok_return_set = QgramTokenizer(return_set=True)
        self.qg3_tok = QgramTokenizer(3)

    def test_qgrams_valid(self):
        self.assertEqual(self.qg2_tok.tokenize(''), [])
        self.assertEqual(self.qg2_tok.tokenize('a'), [])
        self.assertEqual(self.qg2_tok.tokenize('aa'), ['aa'])
        self.assertEqual(self.qg2_tok.tokenize('database'),
                         ['da', 'at', 'ta', 'ab', 'ba', 'as', 'se'])
        self.assertEqual(self.qg2_tok.tokenize('aabaabcdba'),
                         ['aa', 'ab', 'ba', 'aa', 'ab', 'bc', 'cd', 'db', 'ba'])
        self.assertEqual(self.qg2_tok_return_set.tokenize('aabaabcdba'),
                         ['aa', 'ab', 'ba', 'bc', 'cd', 'db'])
        self.assertEqual(self.qg1_tok.tokenize('d'), ['d'])
        self.assertEqual(self.qg3_tok.tokenize('database'),
                         ['dat', 'ata', 'tab', 'aba', 'bas', 'ase'])

    def test_get_return_set(self):
        self.assertEqual(self.qg2_tok.get_return_set(), False)
        self.assertEqual(self.qg2_tok_return_set.get_return_set(), True)

    def test_get_qval(self):
        self.assertEqual(self.qg2_tok.get_qval(), 2)
        self.assertEqual(self.qg3_tok.get_qval(), 3)

    def test_set_return_set(self):
        tok = QgramTokenizer()
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('aabaabcdba'),
                         ['aa', 'ab', 'ba', 'aa', 'ab', 'bc', 'cd', 'db', 'ba'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(tok.tokenize('aabaabcdba'),
                         ['aa', 'ab', 'ba', 'bc', 'cd', 'db'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('aabaabcdba'),
                         ['aa', 'ab', 'ba', 'aa', 'ab', 'bc', 'cd', 'db', 'ba'])

    def test_set_qval(self):
        tok = QgramTokenizer()
        self.assertEqual(tok.get_qval(), 2)
        self.assertEqual(tok.tokenize('database'),
                         ['da', 'at', 'ta', 'ab', 'ba', 'as', 'se'])
        self.assertEqual(tok.set_qval(3), True)
        self.assertEqual(tok.get_qval(), 3)
        self.assertEqual(tok.tokenize('database'),
                         ['dat', 'ata', 'tab', 'aba', 'bas', 'ase'])

    @raises(TypeError)
    def test_qgrams_none(self):
        self.qg2_tok.tokenize(None)

    @raises(AssertionError)
    def test_qgrams_invalid1(self):
        invalid_qg_tok = QgramTokenizer(0) 

    @raises(TypeError)
    def test_qgrams_invalid2(self):
        self.qg2_tok.tokenize(99)

    @raises(AssertionError)
    def test_set_qval_invalid(self):
        qg_tok = QgramTokenizer()
        qg_tok.set_qval(0)


class DelimiterTokenizerTestCases(unittest.TestCase):
    def setUp(self):
        self.delim_tok1 = DelimiterTokenizer()
        self.delim_tok2 = DelimiterTokenizer(set([',']))
        self.delim_tok3 = DelimiterTokenizer(set(['*', '.']))
        self.delim_tok4 = DelimiterTokenizer(set(['..', 'ab']))    
        self.delim_tok4_list = DelimiterTokenizer(['..', 'ab', '..'])
        self.delim_tok4_return_set = DelimiterTokenizer(set(['..', 'ab']),
                                                        return_set=True)

    def test_delimiter_valid(self):
        self.assertEqual(self.delim_tok1.tokenize('data science'),
                         ['data', 'science'])
        self.assertEqual(self.delim_tok2.tokenize('data,science'),
                         ['data', 'science'])
        self.assertEqual(self.delim_tok2.tokenize('data science'),
                         ['data science'])
        self.assertEqual(self.delim_tok3.tokenize('ab cd*ef.*bb. gg.'),
                         ['ab cd', 'ef', 'bb', ' gg'])
        self.assertEqual(
            self.delim_tok4.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', ' cd', 'ef', 'gh'])
        self.assertEqual(
            self.delim_tok4_list.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', ' cd', 'ef', 'gh'])
        self.assertEqual(
            self.delim_tok4_return_set.tokenize(
                'ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', 'gh'])

    def test_get_return_set(self):
        self.assertEqual(self.delim_tok4.get_return_set(), False)
        self.assertEqual(self.delim_tok4_return_set.get_return_set(), True)

    def test_get_delim_set(self):
        self.assertSetEqual(self.delim_tok1.get_delim_set(), {' '})
        self.assertSetEqual(self.delim_tok3.get_delim_set(), {'*', '.'})
        self.assertSetEqual(self.delim_tok4_list.get_delim_set(), {'..', 'ab'})

    def test_set_return_set(self):
        tok = DelimiterTokenizer(set(['..', 'ab']))
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(
            tok.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', ' cd', 'ef', 'gh'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(
            tok.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', 'gh'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(
            tok.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', ' cd', 'ef', 'gh'])

    def test_set_delim_set(self):
        tok = DelimiterTokenizer(['*', '.'])
        self.assertSetEqual(tok.get_delim_set(), {'*', '.'})
        self.assertEqual(tok.tokenize('ab cd*ef.*bb. gg.'),
                         ['ab cd', 'ef', 'bb', ' gg'])      
        self.assertEqual(tok.set_delim_set({'..', 'ab'}), True)
        self.assertSetEqual(tok.get_delim_set(), {'..', 'ab'})
        self.assertEqual(
            tok.tokenize('ab cd..efabbb....ggab cd..efabgh'),
            [' cd', 'ef', 'bb', 'gg', ' cd', 'ef', 'gh'])

    @raises(TypeError)
    def test_delimiter_invalid1(self):
        invalid_delim_tok = DelimiterTokenizer(set([',', 10]))

    @raises(TypeError)
    def test_delimiter_invalid2(self):
        self.delim_tok1.tokenize(None)

    @raises(TypeError)
    def test_delimiter_invalid3(self):
        self.delim_tok1.tokenize(99)


class WhitespaceTokenizerTestCases(unittest.TestCase):
    def setUp(self):
        self.ws_tok = WhitespaceTokenizer()
        self.ws_tok_return_set = WhitespaceTokenizer(return_set=True)

    def test_whitespace_tok_valid(self):
        self.assertEqual(self.ws_tok.tokenize('data science'),
                         ['data', 'science'])
        self.assertEqual(self.ws_tok.tokenize('data        science'),
                         ['data', 'science'])
        self.assertEqual(self.ws_tok.tokenize('data   science'),
                         ['data', 'science'])
        self.assertEqual(self.ws_tok.tokenize('data\tscience'),
                         ['data', 'science'])
        self.assertEqual(self.ws_tok.tokenize('data\nscience'),
                         ['data', 'science'])
        self.assertEqual(self.ws_tok.tokenize('ab cd ab bb cd db'),
                         ['ab', 'cd', 'ab', 'bb', 'cd', 'db'])
        self.assertEqual(self.ws_tok_return_set.tokenize('ab cd ab bb cd db'),
                         ['ab', 'cd', 'bb', 'db'])

    def test_get_return_set(self):
        self.assertEqual(self.ws_tok.get_return_set(), False)
        self.assertEqual(self.ws_tok_return_set.get_return_set(), True)

    def test_set_return_set(self):
        tok = WhitespaceTokenizer()
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('ab cd ab bb cd db'),
                         ['ab', 'cd', 'ab', 'bb', 'cd', 'db'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(tok.tokenize('ab cd ab bb cd db'),
                         ['ab', 'cd', 'bb', 'db'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('ab cd ab bb cd db'),
                         ['ab', 'cd', 'ab', 'bb', 'cd', 'db'])

    def test_get_delim_set(self):
        self.assertSetEqual(self.ws_tok.get_delim_set(), {' ', '\t', '\n'})

    @raises(TypeError)
    def test_whitespace_tok_invalid1(self):
        self.ws_tok.tokenize(None)

    @raises(TypeError)
    def test_whitespace_tok_invalid2(self):
        self.ws_tok.tokenize(99)

    @raises(AttributeError)
    def test_set_delim_set(self):
        self.ws_tok.set_delim_set({'*', '.'})


class AlphabeticTokenizerTestCases(unittest.TestCase):
    def setUp(self):
        self.al_tok = AlphabeticTokenizer()
        self.al_tok_return_set = AlphabeticTokenizer(return_set=True)

    def test_alphabetic_tok_valid(self):
        self.assertEqual(self.al_tok.tokenize(''), [])
        self.assertEqual(self.al_tok.tokenize('99'), [])
        self.assertEqual(self.al_tok.tokenize('hello'), ['hello'])
        self.assertEqual(self.al_tok.tokenize('ab bc. cd##de ef09 bc fg ab.'),
                         ['ab', 'bc', 'cd', 'de', 'ef', 'bc', 'fg', 'ab'])
        self.assertEqual(
            self.al_tok_return_set.tokenize('ab bc. cd##de ef09 bc fg ab.'),
            ['ab', 'bc', 'cd', 'de', 'ef', 'fg'])

    def test_get_return_set(self):
        self.assertEqual(self.al_tok.get_return_set(), False)
        self.assertEqual(self.al_tok_return_set.get_return_set(), True)

    def test_set_return_set(self):
        tok = AlphabeticTokenizer()
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('ab bc. cd##de ef09 bc fg ab.'),
                         ['ab', 'bc', 'cd', 'de', 'ef', 'bc', 'fg', 'ab'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(
            tok.tokenize('ab bc. cd##de ef09 bc fg ab.'),
            ['ab', 'bc', 'cd', 'de', 'ef', 'fg'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(tok.tokenize('ab bc. cd##de ef09 bc fg ab.'),
                         ['ab', 'bc', 'cd', 'de', 'ef', 'bc', 'fg', 'ab'])

    @raises(TypeError)
    def test_alphabetic_tok_invalid1(self):
        self.al_tok.tokenize(None)

    @raises(TypeError)
    def test_alphabetic_tok_invalid2(self):
        self.al_tok.tokenize(99)


class AlphanumericTokenizerTestCases(unittest.TestCase):
    def setUp(self):
        self.alnum_tok = AlphanumericTokenizer()
        self.alnum_tok_return_set = AlphanumericTokenizer(return_set=True)

    def test_alphanumeric_tok_valid(self):
        self.assertEqual(self.alnum_tok.tokenize(''), [])
        self.assertEqual(self.alnum_tok.tokenize('#$'), [])
        self.assertEqual(self.alnum_tok.tokenize('hello99'), ['hello99'])
        self.assertEqual(
            self.alnum_tok.tokenize(',data9,(science), data9#.(integration).88!'),
            ['data9', 'science', 'data9', 'integration', '88'])
        self.assertEqual(self.alnum_tok_return_set.tokenize(
                             ',data9,(science), data9#.(integration).88!'),
                         ['data9', 'science', 'integration', '88'])

    def test_get_return_set(self):
        self.assertEqual(self.alnum_tok.get_return_set(), False)
        self.assertEqual(self.alnum_tok_return_set.get_return_set(), True)

    def test_set_return_set(self):
        tok = AlphanumericTokenizer()
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(
            tok.tokenize(',data9,(science), data9#.(integration).88!'),
            ['data9', 'science', 'data9', 'integration', '88'])
        self.assertEqual(tok.set_return_set(True), True)
        self.assertEqual(tok.get_return_set(), True)
        self.assertEqual(
            tok.tokenize(',data9,(science), data9#.(integration).88!'),
            ['data9', 'science', 'integration', '88'])
        self.assertEqual(tok.set_return_set(False), True)
        self.assertEqual(tok.get_return_set(), False)
        self.assertEqual(
            tok.tokenize(',data9,(science), data9#.(integration).88!'),
            ['data9', 'science', 'data9', 'integration', '88'])

    @raises(TypeError)
    def test_alphanumeric_tok_invalid1(self):
        self.alnum_tok.tokenize(None)

    @raises(TypeError)
    def test_alphanumeric_tok_invalid2(self):
        self.alnum_tok.tokenize(99)
