def print_lol(the_list):
    for index in the_list:
        if isinstance(index,list):
            print_lol(index);
        else:
            print(index);
#函数还要先定义。。。
#movies=['jame','jacke','rick',['haha',['aiwo','biezou','shima']]]  # 你好
#print_lol(movies);

