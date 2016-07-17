""" This is the "xinUtil.py" module, and it provides 
print_list() which prints lists that may or may not
include nested lists."""
def print_list(the_list, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_list(each_item, level+1)
        else:
            for tab_step in range(level):
                print("\t", end='')
            print(each_item)
