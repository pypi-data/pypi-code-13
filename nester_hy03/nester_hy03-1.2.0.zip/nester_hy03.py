"""This file is nester.py module, which offer one function called print_lol.
the function print list given by argument"""
def print_lol(the_list, level=0):
	"""At the front of nested list, We will add blank space which is defined by level argument."""
	"""Using self callback function to print nested list"""
	for each_item in the_list:
		if (isinstance(each_item, list)):
			print_lol(each_item, level+1)
		else:
			for num in range(level):
				print("\t",end='')
			print(each_item)
