'''这是'nester.py'模块，提供了print_lol()函数，用来打印列表'''
def print_lol(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tap_stop in range(level):
                print('/t',end='')
            print(each_item)
