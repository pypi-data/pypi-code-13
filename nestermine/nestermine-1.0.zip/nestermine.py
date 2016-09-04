''' this is the netser module'''
def print_lol(the_list):
    '''this is teh nester function'''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)

            
