Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:01:18) [MSC v.1900 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>>"""这是一个输出多层列表的函数""" 
def print_lol(the_list):
	for each_item in the_kist:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
