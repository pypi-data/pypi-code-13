import string

def histogram(string):
	"""

		provide a dict which returns char-wise distribution
	"""
	d = dict()
	for char in string:
		#check deprecated folder for naive
		d[char] = d.get(char,0) + 1
				#	get key , default_value

	return d

def print_hist(h):
	for char in h:
		print char , h[char]

#TODO :
#check for a way to print_hist in order


if __name__ == '__main__':
	inp_str = raw_input("Enter string to obtain histogram : ")
	hist = histogram(inp_str)

	print hist,'\n'
	print_hist(hist)