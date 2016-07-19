import gzip

import pandas as pd

import wrenlab.util
import wrenlab.genome.gff3
from wrenlab.util import memoize

BASE_URL = "ftp://ftp.sanger.ac.uk/pub/gencode/"

def annotation(release):
    url = "{}/Gencode_human/release_{}/gencode.v{}.annotation.gff3.gz"\
            .format(BASE_URL, release, release)
    path = str(wrenlab.util.download(url))
    with gzip.open(path) as h:
        o = wrenlab.genome.gff3.parse(h)
    return o

def ensembl_to_entrez(release):
    url = "{}/Gencode_human/release_{}/gencode.v{}.metadata.EntrezGene.gz"\
            .format(BASE_URL, release, release)
    path = str(wrenlab.util.download(url))
    o = pd.read_csv(path, compression="gzip", sep="\t")
    o.columns = ["EnsemblTranscriptID", "EntrezGeneID"]
    return o

@memoize
def regions(release, type="exon"):
    gff = annotation(release)
    R = gff.regions(type=type)
    M = ensembl_to_entrez(release)
    o = R.merge(M, left_on="name", right_on="EnsemblTranscriptID")
    o.name = o.EntrezGeneID
    return o.drop(M.columns, axis=1).drop_duplicates()
