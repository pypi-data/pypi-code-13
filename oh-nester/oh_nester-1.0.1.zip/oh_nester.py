def print_lol(one_list,level=0):
	for i in one_list:
		if isinstance(i,list):
			print_lol(i,level+1)
		else:
			for _ in range(level):
				print("\t",end=" ")
			print(i)