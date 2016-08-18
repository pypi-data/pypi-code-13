
# coding: utf-8

# # Polymorphisms

# In[2]:

from whatever import *


# In[10]:

y = Chain(10).range.list
print(type(y))
y.value()


# In[11]:

y = Chain(10).range().list()
print(type(y))
y.value()


# In[12]:

y = Chain(10).range(3).list()
print(type(y))
y.value()


# In[13]:

y = Chain(10)[range][list]
print(type(y))
y.value()


# In[14]:

y = Chain(10) | range | list
print(type(y))
y.value()


# In[19]:

y = (_X(10)[range]) - (lambda x: x< 4) | list
print(type(y))
y.value()


# In[ ]:



