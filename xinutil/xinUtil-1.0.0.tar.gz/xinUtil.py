""" This is the "xinUtil.py" module, and it provides 
print_list() which prints lists that may or may not
include nested lists."""
def print_list(the_list):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_list(each_item)
        else:
            print(each_item)
