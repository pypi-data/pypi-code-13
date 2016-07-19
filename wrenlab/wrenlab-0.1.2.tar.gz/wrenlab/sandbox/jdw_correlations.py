import pandas as pd

def top_correlations(C, k=50, include_query=False):
    """
    Arguments
    ---------
    C : :class:`pandas.DataFrame`
        A square similarity matrix.
    k : int, default 50
        The top correlated elements to output.
    include_query : bool, default False
        Whether to include the query element in the similarity search. If so, 
        the query element should always be in the first few columns. This is
        mainly of use as a control.

    Returns
    -------
    A :class:`pandas.DataFrame` with k columns. The index is the query element,
    and the remaining columns are the most similar other elements, in
    descending order of similarity from left to right.
    """
    o = []
    for q in C.index:
        r = C.loc[q,:]
        nn = list(r.sort_values(ascending=False).index)
        if not include_query:
            del nn[nn.index(q)]
        o.append(nn[:k])
    o = pd.DataFrame.from_records(o)
    o.index = C.index
    return o
