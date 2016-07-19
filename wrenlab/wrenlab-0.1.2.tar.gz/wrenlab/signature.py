"""
Signature analysis:

Problem
=======

Given a set of genes with numeric attributes (expression levels) and a
"database" of genes with numeric attributes, signature analysis provides
different methods of assessing the correlation between the two.

A concrete example: given a set of gene fold changes and a database of genes
that are positive and negative regulators of a certain pathway, is this pathway likely
to be up or down-regulated in this experiment?
"""

import pandas as pd
import scipy.stats

def signature_analysis(X, groups, scores):
    X, groups = X.align(groups, axis=1, join="inner")
    X, scores = X.align(scores, axis=0, join="inner")
    Xs = X.apply(lambda x: (x - x.mean()) / x.std(), axis=1)

    # Spearman rho
    if True:
        rho = Xs.apply(lambda x: scipy.stats.spearmanr(x, scores)[0])
        mu = rho.groupby(groups).mean()
        std = rho.groupby(groups).std()
        se = std / groups.value_counts()
        return pd.DataFrame.from_dict({"Mean":mu, "SD":std, "SE": se}).loc[groups.unique(),:]

    #Xss = (Xs.T * scores).T
    #mu = Xss.groupby(groups, axis=1).mean()
    #print(mu.mean())
    #print(Xss.shape)
    #print(X.iloc[:5,:5])
