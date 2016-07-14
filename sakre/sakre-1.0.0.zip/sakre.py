"""This module is called "one.py" which prints the data contained as  nested lists"""
        
def print_lol(the_list,level):
    """This function takes a single argument called "the_list" and
    it prints the data in nested lists recursively"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            for tab_stop in range(level):
                print("\t",end=' ')
            print(each_item)
            
