
# coding: utf-8

# # Polymorphisms

# In[1]:

from whatever import *


# In[16]:

Chain(10).range.list


# In[17]:

Chain(10).range(5).list


# In[19]:

Chain(10)[range](5)[list]


# In[20]:

Chain(10) | range | list


# In[21]:

Chain(10) | partial(range, 5) | list


# ## Shorthand

# In[24]:

_X(10).range.map(lambda x: x**2).list


# In[58]:

_X(10).range(4).map(lambda x: x**2).list


# In[59]:

_X(10).range(4) * (lambda x: x**2) | list


# In[60]:

_X(10).range(4) * (lambda x: x**2) - (lambda x: x< 20) | list


# In[62]:

_X(10).range(2) * (lambda x: x**2) + (lambda x: x< 20) | list

