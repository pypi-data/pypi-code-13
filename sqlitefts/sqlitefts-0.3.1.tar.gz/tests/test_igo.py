# coding: utf-8
from __future__ import print_function, unicode_literals
import os
import sys

import sqlitefts as fts

import pytest
if sys.version_info >= (3, 3) and sys.version_info < (3, 4):
    import jajp_common
    from jajp_common import *  # noqa
else:
    from jajp_common import *  # noqa
igo = pytest.importorskip('igo')


class IgoTokenizer(fts.Tokenizer):
    def __init__(self, path=None):
        self.tagger = igo.tagger.Tagger(path)

    def tokenize(self, text):
        for m in self.tagger.parse(text):
            start = len(text[:m.start].encode('utf-8'))
            yield m.surface, start, start + len(m.surface.encode('utf-8'))


@pytest.fixture
def name():
    return 'igo'


@pytest.fixture
def t():
    return IgoTokenizer(os.getenv('IGO_DICT'))


skippy33 = pytest.mark.skipif(sys.version_info >= (3, 3) and
                              sys.version_info < (3, 4),
                              reason="not work at python3.3")

test_tokenizer_output = skippy33(test_tokenizer_output)
test_match = skippy33(test_match)
test_insert = skippy33(test_insert)
