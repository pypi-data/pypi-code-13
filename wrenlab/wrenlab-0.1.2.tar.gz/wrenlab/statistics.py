import pandas as pd
import scipy.stats

def rank_to_normal(ranks):
    pctile = (ranks - ranks.min() + 1) / (ranks.max() - ranks.min() + 2)
    return pd.Series(scipy.stats.norm.ppf(pctile), index=pctile.index)
