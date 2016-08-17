def printsomething(the_list : list):
	"""
	prints the input list for you
	"""
	for each_item in the_list:
		if isinstance(each_item, list):
			for each_inner in each_item:
				print(each_inner)
		else:
			print(each_item)
