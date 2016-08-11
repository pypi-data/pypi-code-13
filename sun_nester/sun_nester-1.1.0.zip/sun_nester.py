"""mokuai"""
def print_lol(the_list,level):
    """hanshu"""
    for each_list in the_list:
        if isinstance(each_list,list):
            print_lol(each_list,level+1)
        else:
            for tap_stop in range(level):
                print('\t',end='')
            print(each_list)
