'''
This is a practice exercise from page 37 of the book "Head First Python"
It is just illustrating recursion by defining a module that calls itself from within itself.
'''
def print_lol(the_list):
    '''
    Input: a list, which can have lists nested within
    Output: a print of each element within that list including each element within embedded lists.
    '''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)

