#comment1
def list_engine(the_list):
        #comment2
	for each_item in the_list:
		if isinstance(each_item,list):
			list_engine(each_item)
		else:
			print(each_item)
