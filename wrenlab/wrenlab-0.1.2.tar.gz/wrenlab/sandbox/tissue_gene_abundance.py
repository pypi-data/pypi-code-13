import age_atlas

def run():
    A,X = age_atlas.data()
    A = A.copy()
    A = A.ix[A.TissueID.isin(A.TissueID.value_counts().index[:10]),:]
