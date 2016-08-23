"""这是一个打印列表的函数，如果列表中的元素包含一个列表，
也能打印出其中的列表元素，而不是一个列表"""
def print_lol(the_list,indent=False,level=0):

    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='')
            print(each_item)
