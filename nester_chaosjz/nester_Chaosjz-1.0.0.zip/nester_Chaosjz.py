'''This is the standard way to include a multiple-line comment in your code.'''
def print_lol(the_list):
        '''函数参数是表，也可以是嵌套表，函数将会递归打印表中的所有内容，每个表项打印一行'''
        for each_item in the_list:
                if isinstance (each_item,list):
                        print_lol(each_item)
                else:
                        print(each_item)
