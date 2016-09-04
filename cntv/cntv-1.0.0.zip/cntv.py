"""
这是cntv.py模块，提供了一个名为cntv()的函数，这个
函数的作用是打印列表，其中有可能 包含（也可能不包含）嵌套列表
"""

def cntv2(the_list):
"""
这个函数取一个位置参数，名为“the_list”，这可以是任何python列表
（也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项会（递归
地）输出到屏幕上，各数据项各占一行。
"""
	for each_item in the_list:
		if isinstance(each_item, list):
			cntv2(each_item)
		else:
			print(each_item)

