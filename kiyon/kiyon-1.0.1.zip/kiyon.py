"""这是一个打印函数，参数是一个列表，当列表中包含列表时，会回调自身"""
def print_lol(the_list):
	for item in the_list:
		if isinstance(item,list):
			print_lol(item)
		else:
			print(item)