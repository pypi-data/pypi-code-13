import pandas as pd

__all__ = ["GFF3File", "parse"]

def _parse_exon_id(s):
    return s.split(":")[1:]

def _parse_attributes(s):
    o = {}
    for kv in s.split(";"):
        k,v = kv.split("=", 1)
        o[k] = v
    return o

class GFF3File(object):
    def __init__(self, data):
        self.data = data

    @staticmethod
    def parse(handle):
        o = pd.read_csv(handle, sep="\t", comment="#")
        o.columns=[
                "seqid", "source", "type",
                "start", "end", "score", "strand",
                "phase", "attributes"]
        o.attributes = list(map(_parse_attributes, o.attributes))
        return GFF3File(o)

    def regions(self, type="exon"):
        assert type in set(self.data.type)
        A = self.data.ix[self.data.type == type, :].copy()
        id = pd.Series([m.get("ID") for m in A.attributes], index=A.index)
        A["name"] = id
        o = A.loc[:,["seqid", "start", "end", "name", "score", "strand"]]
        o.columns = ["contig", "start", "end", "name", "score", "strand"]
        
        # Convert to 0-indexed BED coordinates
        o.start -= 1
        o.end -= 1
        o = o.ix[(o.end - o.start).abs() >= 1,:]

        if type == "exon":
            transcript_id, exon_index = zip(*list(map(_parse_exon_id, A.name)))
            o.name = transcript_id
            o["exon_index"] = exon_index

        return o

    def __repr__(self):
        return "<GFF3File with {} elements>".format(self.data.shape[0])

parse = GFF3File.parse
