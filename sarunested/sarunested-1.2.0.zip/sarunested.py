""" This is a module that contains a function named nested_lists """

def nested_lists(mylist, level=0):
	""" This function takes a list and prints all the elements of that list through recursive calling. A second argument called 'level' is used to insert tab-stops when a nested list is encountered."""
	
	for each_item in mylist:
		if isinstance(each_item,list):
			nested_lists(each_item, level+1)
		else:
                        for tab_stop in range(level):
                                print("\t", end='')
                        print(each_item)       
