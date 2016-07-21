# nucleotides.py


# Copyright (C) 2016 - Sven E. Templer <sven.templer@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


import sys
import itertools
import copy


def printcount(seq, kmers, head, n, streamo, pos, window):
    out = [ head, str(pos), str(pos + window), 'w.' + str(n) ]
    err = False
    for kmer in kmers:
        xtab = SeqXTable(seq, kmer)
        cnt = xtab.as_list()
        if cnt is None:
            err = True
            break
        out.extend(map(str, cnt))
    if not err:
        out = '\t'.join(out)
        if streamo is None:
            print out
        else:
            streamo.write(out + '\n')


class SeqXTable():

    
    _N = ['A', 'C', 'T', 'G']


    def __init__(self, seq = None, dim = 1, dimtype = 'prod'):
        self.seq = seq
        self.dim = dim
        self.dimtype = dimtype
        self.labels = None
        self.counts = None
        if seq is not None:
            self._update(dim, dimtype)


    def _generate(self, dim = 1, dimtype = 'prod', asdict = False, addN = True):
        ret = copy.deepcopy(SeqXTable._N)
        if dim > 1:
            if dimtype == 'prod':
                ret = [x for x in itertools.product(ret, repeat = dim)]
            elif dimtype == 'perm':
                ret = [x for x in itertools.permutations(ret, dim)]
            elif dimtype == 'comb':
                ret = [x for x in itertools.combinations(ret, dim)]
            else:
                print >> sys.stderr, 'error: invalid dimtype (must be prod, perm or comb)'
                return None
            ret = map(lambda x : ''.join(x), ret)
        ret = sorted(ret)
        if addN:
            ret.append('N')
        if asdict:
            ret = dict.fromkeys(ret, 0)
        return ret


    def _update(self, dim = 1, dimtype = 'prod'):
        if not self.seq is None and not dim > len(self.seq):
            self.labels = self.generate(dim, dimtype, False, True)
            self.counts = dict.fromkeys(self.labels, 0)
            if dim == 1:
                for base in self.seq:
                    self.counts[base] += 1
            elif dim > 1 and dim <= 4:
                for i in range(len(self.seq) - dim):
                    bases = self.seq[i:(i + dim)]
                    if bases in self.counts.keys():
                        self.counts[bases] += 1
                    else:
                        self.counts['N'] += 1
            else:
                print >> sys.stderr, 'error: dim out of range (1 to 4) to permute bases'
                # check if valid for product or combinations

    
    generate = _generate


    def as_list(self):
        if self.counts is None:
            return None
        return [ self.counts[key] for key in self.labels ]


