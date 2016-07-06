"""Testing the module definition header comment.
This is an example file for oraganizing the functions into modules"""

def print_lol(the_list):
    """This method shall print all the items in the list, even if the items
are themselves list"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:            
            print(each_item)
            
