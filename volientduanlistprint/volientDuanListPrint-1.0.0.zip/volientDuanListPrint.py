def print_isList(this_list):
	for each_item in this_list:
		if isinstance(each_item,list):
			print_isList(each_item)
		else:
			print(each_item)
			