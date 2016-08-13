def print_lol(one_list,level):
	for i in one_list:
		if isinstance(i,list):
			print_lol(i,level)
		else:
			for _ in range(level):
				print("\t",end=" ")
			print(i)