""" This is a module that contains a function named nested_lists """

def nested_lists(mylist):
	""" This function takes a list and prints all the elements of that list through recursive calling."""
	
	for each_item in mylist:
		if isinstance(each_item,list):
			nested_lists(each_item)
		else:
                        print(each_item)
