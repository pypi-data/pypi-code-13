from __future__ import print_function

import dask.dataframe as dd
path = "WEIGHTS.csv"

#df = dd.read_csv(path)
#print(df.head())
#print("average fare + tip was: ", df.total_amount.mean().compute())

print("before read")
df = dd.read_csv(path)

print("after read")
df.to_castra('weights.castra', categories=True)
