
'''这是很多很多的注释啊啊啊
    哈哈哈哦哦哦
    耶耶。。。'''
def print_lol(this_list,indent=False,level=0):
    for one in this_list:
        if isinstance(one,list):
            print_lol(one,level+1)
        else:
            if indent:
                for tab in range(level):
                    print('\t',end='')
            print(one)