"""this is the"""
def print_lol(the_list):
    """this function takes one position"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
