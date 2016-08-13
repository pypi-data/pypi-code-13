"""A module with utilities to help with nested item iteration"""
def print_lol(the_list, indent=False, level=0):
    """print_lol is used to iterate through a list to be printed, and ensure that
        any items involved, if lists themselves, are also iterated through for proper 
        text formatting of list items within that list.  This function uses recursions.
        it additionally has a second argument called level, which is used to insert
        tab stops when a nested list is encountered"""
    for list_item in the_list:
        if isinstance(list_item,list):
            print_lol(list_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end="")
            print(list_item)
            
