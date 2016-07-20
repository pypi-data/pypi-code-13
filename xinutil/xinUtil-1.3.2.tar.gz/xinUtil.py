""" This is the "xinUtil.py" module, and it provides 
print_list() which prints lists that may or may not
include nested lists."""
import sys

def print_list(the_list, indent=False, level=0, fh=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_list(each_item, indent, level+1, fh)
        else:
            if indent:
                for tab_step in range(level):
                    print("\t", end='', file=fh)
            print(each_item, end='', file=fh)
