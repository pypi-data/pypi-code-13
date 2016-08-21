""" This is a module that contains a function named nested_lists """

def nested_lists(mylist, indent=False, level=0):
	""" This function takes a list and prints all the elements of that list through recursive calling.
             A second argument called 'level' is used to insert tab-stops when a nested list is encountered. Default is 0 so no problem if second argument is not passed with the call.
             A third argument 'indent' is used to control the behavior of the function, it is default to False so no indentation will occur until an argument 'true' is passed in the argument. """
	
	for each_item in mylist:
		if isinstance(each_item,list):
			nested_lists(each_item, indent, level+1)
		else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t", end='')
                        print(each_item)
