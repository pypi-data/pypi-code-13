'''这是测试函数，可以打印'''
def print_lol(the_list,lv):
    '''参数1是列表值，'''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,lv+1)
        else:
            for num in range (lv):
                    print('\t',end='')
            print(each_item)
            
