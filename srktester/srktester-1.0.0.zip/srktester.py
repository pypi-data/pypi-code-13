"""Sample test function"""
def print_lol(the_list):
    """Prints all the elments in the list including that of inner lists."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)           
