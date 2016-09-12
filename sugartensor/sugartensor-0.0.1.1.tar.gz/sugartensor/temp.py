import joblib
import numpy as np

data = joblib.load('/shared/asan/dild/data/patch.manufac.20x20.pkl')['siemens']

res = []
for klass in data:
    for im in klass:
        res.append(res)
res = np.asarray(res)
##



##