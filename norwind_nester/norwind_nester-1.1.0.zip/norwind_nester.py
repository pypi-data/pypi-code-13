def print_lol(the_list, tabnum):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,tabnum+1);
		else:
			for num in range(tabnum):
				print("\t",end='')
			print(each_item)