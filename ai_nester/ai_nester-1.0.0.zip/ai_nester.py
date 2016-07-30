"""zhis is e function for list,
	you can use it look the yuan of list
"""



def print_lol(the_list):
	""" daima"""
	for each in the_list:
		if isinstance(each,list):
			print_lol(each)
		else:
			print(each)
