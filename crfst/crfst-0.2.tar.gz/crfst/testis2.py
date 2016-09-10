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

import ConfigParser, StringIO

cfg_str = """[tagger]
# Training data path
train=data/test.txt

# Testing data path
test=data/test.txt

# Model path
model=tmp/model

# Feature vector
ftvec=word:[-3:3];can:[-3:3];cls:[0];short

# column separator in input (and output) file(s)
tab_sep=\s

# Column pattern
# [pos <form, postag>, chunk <form, postag, chunktag>]
cols=chunk

# Label column name
label_col=chunktag

# Evaluation function [pos, conll]
# Note: the evaluation functions are not constrained by tagset. However, the
# conll and bio evaluation functions work only with BIO or BIOSE tagsets.
eval_func=bio

# Name for the guess label column
guess_label_col=guesstag

[resources]
# Stanford clusters
cls=data/thesauri/egw4-reut.512.clusters

[crfsuite]
# coefficient for L1 penalty
c1=0.80
# coefficient for L2 penalty
c2=1e-3
# stop earlier
max_iterations=100
# include transitions that are possible, but not observed
feature.possible_transitions=True
"""

sio = StringIO.StringIO(cfg_str)
cfg = ConfigParser.ConfigParser()
cfg.readfp(sio)


def word(data, i, cols, rel=0, *args, **kwargs):
    """Generates a feature based on the `form` column, but replaces some
    prepositions with a placeholder <preposition>.

    **FEATURE GENERATION FUNCTION**

    :param data: data
    :type: np.recarray
    :param i: focus position
    :type i: int
    :param cols: column map
    :type cols: dict
    :param rel: relative position of context features
    :type rel: int
    :return: feature
    :rtype: str
    """
    if 0 <= i + rel < len(data):
        form = data[i + rel][cols['form']]
    else:
        form = None
    if form in ['to', 'from', 'with', 'in', 'over', 'by', 'through']:
        form = '<preposition>'
    return 'w[%s]=%s' % (rel, form)

from crfst.tagger import CRFSTagger
from crfst.utils import parse_tsv, export

c = CRFSTagger(cfg, fnx=[word])
c.train()
r, d = c.test()
print r

word = None
c = CRFSTagger(mp='tmp/model')
data = parse_tsv('data/test.txt', cols='chunk', ts=' ')
d = c.tag(data=data)
export(d, open('tmp/chunk_output.txt', 'w'), cols='chunk')
print d[:5]