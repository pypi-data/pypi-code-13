def islist(list1,level):
	for each_list in list1:
		if isinstance(each_list,list):
			islist(each_list,level+1)
		else:
			for tab_stop in range(level):
				print('\t',end='')
			print(each_list)
