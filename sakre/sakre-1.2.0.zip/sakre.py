"""This module is called "one.py" which prints the data contained as  nested lists"""
        
def print_lol(the_list,indent=False,level=0):
    """This function takes a single argument called "the_list" and
    it prints the data in nested lists recursively"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab in range(level):
                    print("\t",end=' ')
            print(each_item)
            
