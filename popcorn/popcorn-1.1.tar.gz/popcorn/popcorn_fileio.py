'''
Popcorn 1.1
https://github.com/InitializeSahib/Popcorn
'''
def write_string_to_file(filename, string_to_write):
	with open(filename, "wt") as outstr:
		outstr.write(string_to_write)
def read_file(filename):
	with open(filename, "rt") as instr:
		return instr.read()
