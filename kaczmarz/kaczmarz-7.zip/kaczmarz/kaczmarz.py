def kaczmarz(sys, itrs):
	for i in itrs:
		row = sys.A[i, :]
		rej = (row @ row - sys.b[i]) / (row @ row) * row
		sys.x -= rej


