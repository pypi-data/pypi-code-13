"""
*****************************************
***NESTING RECURRING LISTS WITH LEVELS***
*****************************************
"""
def print_lol(list_of_items, level=0):
	for items in list_of_items:
		if(isinstance(items, list)):
			print_lol(items, level+1)
		else:
			for tab_level in range(level):
				print("\t", end='')
			print(items)
