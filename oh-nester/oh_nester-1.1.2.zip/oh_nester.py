def print_lol(one_list,indent=False,level=0):
	for i in one_list:
		if(indent == True):
			if isinstance(i,list):
				print_lol(i,True,level+1)
			else:
					for _ in range(level):
						print("\t",end=" ")
					print(i)
		else:
			print(i);