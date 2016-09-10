"""这是"wester.py"模块，提供了一个名为print_lol的函数，这个函数的作用是打印列表，
其中有可能包含（也有可能不包含）嵌套列表"""
import sys
def print_lol(the_list,indent = False,level=0,fn = sys.stdout):
    """参数the_list可以是任意的列表，所指定的列表中的数据项也会（递归的）输出在屏幕上"""
    for each_item in the_list:        
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1,fn)           
        else:
            if indent:                
                for tab_stop in range(level):
                    print('\t',end=' ',file = fn)
                print(each_item ,file = fn)

