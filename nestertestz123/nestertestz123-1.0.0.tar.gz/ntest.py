"""这是nester.py模块，提供了一个名为print_lol的函数，这个函数的作用是打印列表，其中可能包含也可能不包含嵌套列表"""
def print_lol(the_list):
	"""函数取一个位置参数，名为the_list，这可能是任何python的列表，也可以包含嵌套列表，所指定的每个列表项将会递归的显示到屏幕上，各数据项各占一行"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
