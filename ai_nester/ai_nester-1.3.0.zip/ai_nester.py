"""zhis is e function for list,
	you can use it look the yuan of list
"""



def print_lol(the_list,indent=Flase,len=0):
	# daima
	for each in the_list:
		if isinstance(each,list):
			print_lol(each,indent,len+1)
		else:
			if indent:
				for is_len in range(len):
				 	print("\t",end='')
			print(each)
