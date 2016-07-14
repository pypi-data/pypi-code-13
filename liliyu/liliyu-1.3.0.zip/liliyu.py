"""这是‘nester.py’模块，提供一个名为‘print_lol'的函数，这个函数的作用是打印列表（也可以是包含
嵌套列表的列表）。"""
# nester.py
def print_lol(the_list,indent = False,level = 0):
    """这个函数取一个位置参数，名为'the_list’,这可以是任何python列表（也可以是
包含嵌套列表的列表）。所指定的列表中的每个数据项都会（递归地）输出到屏幕上，各
数据项占一行;第二个参数（indent）,默认值为False,各项列举时没有缩进；最后一个参数（level），使各项可以根据嵌套层数缩进;"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end = '')
            print(each_item)
