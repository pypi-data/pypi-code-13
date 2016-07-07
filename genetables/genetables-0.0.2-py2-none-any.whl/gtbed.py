# bed.py


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


from pybedtools import BedTool as as_bed


### is_featuretype

# feature = string, e.g. 'exon', etc
# featuretype =

def is_featuretype(feature, featuretype):
    if feature[2] == featuretype:
        return True
    return False


### subset_featuretype

# featuretype = 
# gtf =

def subset_featuretype(featuretype, gtf):
    r = gtf.filter(is_featuretype, featuretype).saveas()
    return BedTool(r)


### get_chrom

# gtf =

def get_chrom(gtf):
    chromosomes = set()
    for i in gtf:
        chromosomes.add(i[0])
    return chromosomes


