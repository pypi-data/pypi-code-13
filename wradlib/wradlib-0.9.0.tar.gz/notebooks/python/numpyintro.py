
# coding: utf-8

# This notebook is part of the $\omega radlib$ documentation: http://wradlib.org/wradlib-docs.
# 
# Copyright (c) 2016, $\omega radlib$ developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

# # NumPy: manipulating numerical data

# *NumPy* is the key Python package for creating and manipulating (multi-dimensional) numerical arrays. *NumPy* arrays are also the most important data objects in $\omega radlib$. It has become a convention to import *NumPy* as follows:

# In[ ]:

import numpy as np


# ## Creating and inspecting NumPy arrays
# 
# The `ndarray`, a numerical array, is the most important data type in NumPy. 

# In[ ]:

a = np.array([0, 1, 2, 3])
print(a)
print(type(a))


# You can inspect the `shape` (i.e. the number and size of the dimensions of an array).

# In[ ]:

print(a.shape)
# This creates a 2-dimensional array
a2 = np.array([[0, 1], [2, 3]])
print(a2.shape)


# There are various ways to create arrays: from lists (as above), using convenience functions, or from file.

# In[ ]:

# From lists
a = np.array([0, 1, 2, 3])
print("a looks like:\n%r\n" % a)

# Convenience functions
b = np.ones( shape=(2,3) )
print("b looks like:\n%r\nand has shape %r\n" % (b, b.shape) )

c = np.zeros( shape=(2,1) )
print("c looks like:\n%r\nand has shape %r\n" % (c, c.shape) )

d = np.arange(2,10)
print("d looks like:\n%r\nand has shape %r\n" % (d, d.shape) )

e = np.linspace(0,10,5)
print("e looks like:\n%r\nand has shape %r\n" % (e, e.shape) )


# You can change the shape of an array without changing its size.

# In[ ]:

a = np.arange(10)
b = np.reshape(a, (2,5))
print("Array a has shape %r.\nArray b has shape %r" % (a.shape, b.shape))

