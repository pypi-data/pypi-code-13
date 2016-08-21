"""this is a module named 'nester_wiki' to display the content of a list with or without a sublist"""
def print_lol(the_list, intend=False,level=0):
	for each_item in the_list:
		if isinstance (each_item, list):
			print_lol(each_item, intend,level+1)
		else:
			if intend:
				print("\t"*level,end='')
			print(each_item)
