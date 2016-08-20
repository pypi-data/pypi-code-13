"""This is the "LiStatham_nester.py" moudle and it provides one function called print_lol() which prints lists that may or may not include nested lists."""

def print_lol(the_list, level=0):
    """This function takes one positional argument called "the_list", which is any Python list (of - possibly - nested lists). Each data item in the provided list is (recursively) printed to the screen on it's own line. The second parameter called the "level" is used to insert TAB when meets nested lists."""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
