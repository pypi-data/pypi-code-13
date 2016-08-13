def print_lol(one_list):
	for i in one_list:
		if isinstance(i,list):
			print_lol(i)
		else:
			print(i)