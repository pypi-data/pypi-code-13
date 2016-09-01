
'''这是很多很多的注释啊啊啊
    哈哈哈哦哦哦
    耶耶。。。'''
def print_lol(this_list,level):
    for one in this_list:
        if isinstance(one,list):
            print_lol(one,level+1)
        else:
            for tab in range(level):
                print('\t',end='')
            print(one)