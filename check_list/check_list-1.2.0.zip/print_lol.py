#Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32
#Type "copyright", "credits" or "license()" for more information.
#function "print_lol" will display every list element in each row,loop element list with fuction itself.
def print_lol(the_list):
	for element in the_list:
		if isinstance(element,list):
			print_lol(element)
		else:
			print(element)

#function "print_lola" displays all elements with "space" times tab"\t" in single row.loop element with function itself.
def print_lola(the_list1,space):
	for element1 in the_list1:
		if isinstance(element1,list):
			print_lola(element1,space)
		else:
			for times in range(space):
				print("\t",end=element1)


#for sample test: cast=['dfd', 'dfsf', ["dfdq", "123","3434"], 'dfds', [["reerr","rere","trtrr"], 'sgfgfg', 'gr']]
				
