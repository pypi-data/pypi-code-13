from recordclass import recordclass
import numpy as np

def kaczmarz(sys, itrs):
	for i in itrs:
		row = sys.A[i, :]
		rej = (row @ sys.x - sys.b[i]) / (row @ row) * row
		sys.x -= rej