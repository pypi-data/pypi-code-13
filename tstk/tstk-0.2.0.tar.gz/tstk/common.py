compnt = {'A':'T','C':'G','G':'C','T':'A','N':'N'}

revcomp = lambda x: ''.join([compnt[B] for B in x][::-1])

def featurecountsdf(fname,allcolumns=False):
    import pandas as pd

    df = pd.read_table(fname,sep="\t",header=1) 
    if not allcolumns:
        cols = ["Geneid"] + [c for c in df.columns[df.columns.get_loc("Length"):]]
        df = df[cols]

    return df
