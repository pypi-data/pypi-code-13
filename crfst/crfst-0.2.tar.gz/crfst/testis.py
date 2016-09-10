# This file is part of CRFSuiteTagger.
#
# CRFSuiteTagger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CRFSuiteTagger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CRFSuiteTagger.  If not, see <http://www.gnu.org/licenses/>.
__author__ = 'Aleksandar Savkov'

import logging, os
from configparser import ConfigParser
from crfst.tagger import CRFSTagger
from crfst.utils import parse_tsv, export


def make_cfg(
    train='/home/sasho/Apollo/Harvey/chunks/ark/nabu-sample1-train.data',
    test='/home/sasho/Apollo/Harvey/chunks/ark/nabu-sample1-test.data',
    model='/home/sasho/tmp/crfs/model',
    ftvec='word:[-3:3];can:[-3:3];pos:[-3:3];isnum:[-3:3];short',
    tab_sep='\\s',
    cols='chunk',
    label_col='chunktag',
    eval_func='conll',
    guess_label_col='guesstag',
    verbose=True,
    cls=None,
    emb=None,
    brown=None,
    c1=0.80,
    c2=1e-3,
    max_iterations=100,
    ft_possible_transitions=True
):
    c = ConfigParser()
    c.add_section('tagger')
    c.set('tagger', 'train', train)
    c.set('tagger', 'test', test)
    c.set('tagger', 'model', model)
    c.set('tagger', 'ftvec', ftvec)
    c.set('tagger', 'tab_sep', tab_sep)
    c.set('tagger', 'cols', cols)
    c.set('tagger', 'label_col', label_col)
    c.set('tagger', 'eval_func', eval_func)
    c.set('tagger', 'guess_label_col', guess_label_col)
    c.set('tagger', 'verbose', str(verbose))

    c.add_section('resources')
    if cls:
        c.set('resources', 'cls', cls)
    if emb:
        c.set('resources', 'emb', emb)
    if brown:
        c.set('resources', 'brown', brown)

    c.add_section('crfsuite')
    c.set('crfsuite', 'c1', str(c1))
    c.set('crfsuite', 'c2', str(c2))
    c.set('crfsuite', 'max_iterations', str(max_iterations))
    c.set('crfsuite', 'feature.possible_transitions', str(ft_possible_transitions))

    return c

if __name__ == '__main__':
    cfg = make_cfg(
        train='',
        test='',
        verbose='',
        eval_func='bio',
        # emb='/home/sasho/Apollo/fast_wordrep/WordEmbedding/hlbl/hlbl-embeddings-scaled.EMBEDDING_SIZE=100.txt',
        brown='/home/sasho/Apollo/fast_wordrep/Brown/biomed/c1000.txt',
        ftvec='word:[-1:1];pos:[-1:1];npos:[-1:1];brown:[0];short'
    )
    cfg.set('tagger', 'form_col', 'form2')
    c = CRFSTagger(cfg, cols={'form':'form2', 'postag':'postag', 'chunktag':'chunktag'})
    # c.cfg.set('crfsuite', 'feature.minfreq', '1')
    # c.cfg.set('resources', 'emb', '/home/sasho/Apollo/fast_wordrep/WordEmbedding/gprd/word2vec.100.drtokenized.txt')
    print 'loaded'
    from utils import parse_tsv, cv_splits
    from crfst. eval import conll
    data = parse_tsv('/home/sasho/Apollo/Harvey/chunks/ark/nabu-all.data', cols=('form2', 'postag', 'chunktag'), ts=' ')
    res = []
    res2 = []
    import pickle
    for i, (trd, ted) in enumerate(cv_splits(data, 10)):
        print len(trd), len(ted)
        c.train(data=trd, dump=False)
        info = c.info()
        r, d = c.test(data=ted)
        r2 = conll(d)
        info = c.info()
        print r, r2
        res.append(r)
        res2.append(r2)
    import numpy as np
    print np.mean([x['Total']['fscore'] for x in res]), np.mean([x['Total']['fscore'] for x in res2])