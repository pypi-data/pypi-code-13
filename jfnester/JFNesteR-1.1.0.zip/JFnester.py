'''
This is a practice exercise from pages 37 and 55 of the book "Head First Python"
It is just illustrating recursion by defining a module that calls itself from within itself.
'''
def print_lol(the_list, in_depth):
    '''
    Input: a list, which can have lists nested within
    Output: a print of each element within that list including each element within embedded lists.
    Parameters:
       1) the list that is to be printed out
       2) the depth to which indents should be done
    '''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, in_depth+1)
        else:
            for ind in range(in_depth):
                print("\t", end='')
            print(each_item)

