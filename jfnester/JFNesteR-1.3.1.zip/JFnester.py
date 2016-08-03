'''
This is a practice exercise from pages 37 and 55 of the book "Head First Python"
It is just illustrating recursion by defining a module that calls itself from within itself.
'''
def print_lol(the_list, indent_TorF=False, tab_depth=0):
    '''
    Input: a list, which can have lists nested within
    Output: a print of each element within that list including each element within embedded lists.
    Parameters:
       1) the list that is to be printed out
       2) a boolean to indicate whether or not indentation should be used at all
       3) the depth to which indents should be done
    '''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent_TorF, tab_depth+1)
        else:
            if indent_TorF:
                for ind in range(tab_depth):
                    print("\t", end='')
            print(each_item)

