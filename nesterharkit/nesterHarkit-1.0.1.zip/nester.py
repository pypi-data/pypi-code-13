print("Nester imported")
print()
""" This module is used to demostrate the recursive funtion."""
def print_lol(the_list, level):

    """ This function will recursively iterate through the list and any nested
lists to print the items in those lists with indentations"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)
