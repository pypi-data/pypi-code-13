def tt(ee):
	for each in ee:
		if isinstance(each,list):
			tt(each)
		else:
			print(each)

