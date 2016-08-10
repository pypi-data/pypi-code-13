"""This is the "standard" way to include a multiple-line comment in your code."""

# This is a single line comment

def print_list(the_list, level):
	for item in the_list:
		if isinstance(item, list):
			print_list(item, level + 1)
		else:
			i = 0
			result = ""
			while i < level:
				result += " "
				i = i + 1
			result = result + item
			print(result)

