'''This is my first Python code.
    And it is a nest print function.'''

def print_lol(the_list):
    '''The function name is print_lol that can print list nestly.
   the_list is the format arguments, its type is List.
   It will print each item from list one by one line.'''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
    
