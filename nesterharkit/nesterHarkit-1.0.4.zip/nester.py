print("Nester imported Version 1.0.4")
print()
""" This module is used to demostrate the recursive funtion."""
def print_lol(the_list, indent=False, level=0, fh=sys.stdout):

    """ This function will recursively iterate through the list and any nested
lists to print the items in those lists with indentations"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='', file=fh)
            print(each_item, file=fh)
