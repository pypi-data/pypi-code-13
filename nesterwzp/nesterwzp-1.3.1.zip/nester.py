'''This is my first Python code.
    And it is a nest print function.'''

def print_lol(the_list,indent=False,level=0):
    '''The function name is print_lol that can print list nestly.
   the_list is the format arguments, its type is List.
   It will print each item from list one by one line.'''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='')
#                    print(tab_stop)
            print(each_item)
    
