
'''这是很多很多的注释啊啊啊
    哈哈哈哦哦哦
    耶耶。。。'''
def print_lol(this_list):
    for one in this_list:
        if isinstance(one,list):
            print_lol(one)
        else:
            print(one)