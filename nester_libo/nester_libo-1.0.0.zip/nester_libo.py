'''
Thia is the 'nester.py' moudle and it provide one function called print_lol()
which prints lists that may not include lists.
'''
def print_lol(the_list):
    '''
This function takes one positional argument called 'the list',which is any Python list.
Each data item in the provied list id printed to the screen on it's own line.
'''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print each-item


