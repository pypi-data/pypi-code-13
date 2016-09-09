def print_lol(the_list,indent=False,level=0):
	'''打印嵌套列表的函数，可以用参数控制缩进，默认为不缩进'''
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='')
			print(each_item)