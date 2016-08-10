"""This is the "standard" way to include a multiple-line comment in your code."""

# This is a single line comment

def print_list(the_list):
	for item in the_list:
		if isinstance(item, list):
			print_list(item)
		else:
			print(item)