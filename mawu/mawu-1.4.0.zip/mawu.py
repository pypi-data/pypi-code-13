import sys
"""This is the "mawu.py" module, and it provides one function called
great_start() which prints lists that may or may not include nested lists"""

def great_start(the_list, level=0, fh=sys.stdout):
    """This function takes one positional argument called "the_list", which
is any python list (of - possibly - nested lists). Each data item in the
provided list is (recursively) printed to the screen on it's own line.
A second argument called "level" is used to insert tab-stops when a nested
list is encounted."""
    for each_item in the_list:
        if isinstance(each_item, list):
            great_start(each_item, level+1, fh)
        else:
            for tab_stop in range(level):
                print("\t", end='', file=fh)
            print(each_item, file=fh)
