import numpy as np
import indices_utils

N=20
n=3
for id in range(10):
    indices=range(0,N,n)
    #indices=np.sort(np.random.choice(range(N),size=n,replace=False))

    slices=indices_utils.convert_indices_to_slices_fix(indices)
    if np.any(np.sort(np.concatenate([np.arange(N)[simple_slice] for simple_slice in slices]))-indices)!=0:
        print(indices)

