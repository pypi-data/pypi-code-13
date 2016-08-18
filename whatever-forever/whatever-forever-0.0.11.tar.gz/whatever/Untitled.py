
# coding: utf-8

# In[1]:

from whatever import *
from time import time


# In[5]:

from sklearn.datasets import load_digits


# In[10]:

import pandas


# In[14]:

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


# In[19]:

model = LinearDiscriminantAnalysis()
(_X(load_digits)
 | this()().f
 | get(['data','target'])
 | (lambda x: pandas.DataFrame(x[0], index=x[1]))
 | this().drop_duplicates().f
 | do(lambda x: model.fit(x.values, x.index))
 | this().values.f
 | model.predict
)


# In[20]:

with open() as f: s = f.read()


# In[22]:

from nbconvert import export_script


# In[33]:

_X('chain.ipynb') | export_script | first | str.splitlines | filter(bool) | filter(
    complement(this().lstrip().startswith('#').f)
) | filter(
    complement(this().lstrip().startswith('@').f)
) | list | do(_X().len.print.f)| '\n'.join > print


# In[ ]:



