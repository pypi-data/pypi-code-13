"""This is the "nester.py" moudle and it provides one function called print_lol(), which print 	    lists that may or may not include nested lists:"""

def print_lol(the_list,level):
	"""This function takes one positional argument called "the_list", which is any python 		   list. Each data item in the provided list is printed to the screen on it's own line.
	"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for tab_num in range(level):
				print("\t",end='')
			
			print(each_item)
