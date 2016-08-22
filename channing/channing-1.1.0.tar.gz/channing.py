def lol(the_list,level):
	for each_item in the_list:
		if isinstance (each_item,list):
			lol (each_item,level+1)
		else:
			for tab_stop in range(level):
				print("\t",end="")
			print (each_item)