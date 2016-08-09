"""Sample test function"""
def print_lol(the_list, level=0):
    """Prints all the elments in the list including that of inner lists."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,level + 1)
        else:
            for tab_stop in range(level):                
                print("\t",end='')
            print(each_item)
