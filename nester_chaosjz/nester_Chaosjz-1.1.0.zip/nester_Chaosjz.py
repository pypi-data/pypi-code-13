'''This is the standard way to include a multiple-line comment in your code.'''
def print_lol(the_list,level):
        '''函数的第一个参数是the_list，格式是python数据表，也可以是嵌套表，函数的第二个参数为是level，格式为数字，代表发生嵌套表时缩进的次数函数将会递归打印表中的所有内容，每个表项打印一行'''
        for each_item in the_list:
                if isinstance (each_item,list):
                        print_lol(each_item,level+1)
                else:
                        for num in range(level):
                                print('\t',end='')
                        print(each_item)
