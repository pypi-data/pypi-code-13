"""This is nester.py module, V1.5.0"""
def print_lol(the_list, level=0):
    """This function print a list dada"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
