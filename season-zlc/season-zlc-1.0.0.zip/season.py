"""This is the standard way to 
	include a multiple-line comment in
	your code"""
	
def print_lol(the_list):
	"""this function print list"""
	for each in the_list:
		if isinstance(each,list):
			print_lol(each)
		else:
			print(each)