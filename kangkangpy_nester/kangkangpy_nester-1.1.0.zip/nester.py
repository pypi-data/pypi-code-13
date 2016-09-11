""" 这是"nester.py"模块，提供了一个名为pint_lol()的函数，这个函数的作用是打印列表，
    其中有可能包含嵌套列表。"""
def print_lol(the_list,TAB_num):
    """ 这个函数去一个位置参数，名为“the_list”，这个是任何python列表（也可以是
    包含嵌套列表的列表）。所指定的列表中的每一个数据项会（递归地）输出到屏幕上，
    各数据各占一行。"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,TAB_num+1)))
        else:
            for num in range(TAB_num):
                print("\t",end='')
            print(each_item)
