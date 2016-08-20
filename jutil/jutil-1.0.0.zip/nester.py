""" 
this is a util funciton set writern by Jetty
"""
def printlol(arr):
	"""
	this function print nested list
	"""
	for item in arr:
		if isinstance(item, list):
			printlol(item)
		else:
			print(item)
