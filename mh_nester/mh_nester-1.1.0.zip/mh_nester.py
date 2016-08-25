"""这是一个"nester.py"模块，提供了一个命名为print_lol()的函数，函数的作用是打印列表内容，
列表中可能包含嵌套列表"""
def print_lol(the_list，level):
    """这个函数取一个位置参数，命名为the_list，可以为任意一个python列表或嵌套列表，指定
列表中的每一个数据项会递归出现在屏幕上，每个数据各占一行。"""
    """level 参数是用来遇到嵌套列表时输出制表符"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print('\t',end='')    """表示输出的字符为制表符，python默认为简单换行"""
            print(each_item)

            
