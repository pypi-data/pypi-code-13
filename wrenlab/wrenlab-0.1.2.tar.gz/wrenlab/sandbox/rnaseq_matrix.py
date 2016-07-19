import os.path
import glob

import pandas as pd

from wrenlab.genome import BigWigFile
from wrenlab.util import LOG

class BigWigCollection(object):
    def __init__(self, root, extension=".bw"):
        self._root = root
        self._extension = extension
        self._pmap = {}
        self._hmap = {}

        for path in glob.glob(os.path.join(root, "*{}".format(self._extension))):
            sample_id = os.path.splitext(os.path.basename(path))[0]
            self._pmap[sample_id] = path
            self._hmap[sample_id] = BigWigFile(path)

    @property
    def samples(self):
        return self._pmap.keys()

    def query(self, contig, start, end):
        o = []
        for sample_id, bw in self._hmap.items():
            o.append(bw.summarize_region(contig, start, end).mean0)
        return pd.Series(o, index=list(self.samples))

class StrandSpecificBigWigCollection(object):
    def __init__(self, root, extension=".bw"):
        fwd_dir = os.path.join(root, "fwd")
        rev_dir = os.path.join(root, "rev")
        self._fwd = BigWigCollection(fwd_dir, extension=extension)
        self._rev = BigWigCollection(rev_dir, extension=extension)
        self._samples = list(sorted(set(self._fwd.samples) & set(self._rev.samples)))

    def query(self, contig, start, end, strand):
        assert strand in ("+", "-")
        if strand == "+":
            return self._fwd.query(contig, start, end).loc[self._samples]
        elif strand == "-":
            return self._rev.query(contig, start, end).loc[self._samples]
        else:
            raise AssertionError
     

def _counts(root, annotation, bigwig_ext=".bw"):
    annotation = annotation.ix[annotation.strand.isin(["+","-"]),:]

    fwd = os.path.join(root, "fwd")
    rev = os.path.join(root, "rev")
    fwd_files = set(map(os.path.basename, glob.glob(os.path.join(fwd, "*{}".format(bigwig_ext)))))
    rev_files = set(map(os.path.basename, glob.glob(os.path.join(rev, "*{}".format(bigwig_ext)))))

    samples = list(sorted(map(lambda x: os.path.splitext(x)[0], fwd_files & rev_files)))
    O = []

    for sample_id in samples:
        o = {}
        try:
            bws = {
                "+": BigWigFile(os.path.join(root, "fwd", "{}{}".format(sample_id, bigwig_ext))),
                "-": BigWigFile(os.path.join(root, "rev", "{}{}".format(sample_id, bigwig_ext)))
            }
        except AssertionError:
            LOG.warn("Unable to open BigWig file for sample: {}".format(sample_id))
            continue

        for strand, A in annotation.groupby("strand"):
            bw = bws[strand]
            for gene_id, A_gene in A.groupby("name"):
                total_length = (A_gene.end - A_gene.start).abs().sum()
                mu = []
                for ctg, start, end in A_gene.loc[:,["contig","start","end"]].to_records(index=False):
                    if start == end:
                        continue
                    start, end = sorted([start, end])
                    mu.append(bw.summarize_region(ctg, start, end).mean0 * abs(end - start))
                o[gene_id] = sum(mu) / total_length
            o = pd.Series(o)
            o.name = sample_id
            O.append(o)
    return pd.concat(O, axis=1)
