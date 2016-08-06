""" This is my firt  module python"""
def print_lol(the_list):
    """Recursive list iteration"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)