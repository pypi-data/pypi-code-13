def print_isList(this_list,level):
	for each_item in this_list:
		if isinstance(each_item,list):
			print_isList(each_item,level+1)
		else:
			for tab_v in range(level):
				print("\t",end='')
			print(each_item)
			