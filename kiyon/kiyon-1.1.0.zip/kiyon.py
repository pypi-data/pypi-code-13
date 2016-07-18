"""这是一个打印函数，参数是一个列表，当列表中包含列表时，会回调自身"""
def print_lol(the_list,level=0):
	for item in the_list:
		if isinstance(item,list):
			print_lol(item,level+1)
		else:
			for num in range(level):
				print('\t',end='')
			print(item)