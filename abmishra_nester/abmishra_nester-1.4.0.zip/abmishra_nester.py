"""This is the "abmishra_nester.py" module and it provides one function
called print_lol() which prints lists that may or may not include nested
lists."""

def print_lol(the_list, indent = False, level = 0, data_file=sys.stdout):
        """This function takes one positional argument called "the_list", which
        is any Python list (of - possibly - nested lists). Each data
        item in the provided list is (recursively) printed to the screen
        on its own line. A second argument "level" is used to instert
        tab-stops when a nested list is encountered"""
        for each_item in the_list:
                if isinstance(each_item, list):
                        print_lol(each_item, indent, level+1, data_file)
                else:
                        if indent:
                                print("\t"*level, end='', file=data_file)
                        print(each_item, file=data_file)
