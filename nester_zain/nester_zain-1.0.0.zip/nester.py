def print_lol(movies):
	for each_item in movies:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
