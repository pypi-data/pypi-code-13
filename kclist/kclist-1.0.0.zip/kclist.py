
#慢方法
"""for each_item in number:
    if isinstance(each_item,list):
        for nested_item in each_item:
            if isinstance(nested_item ,list):
                for deeper_item in nested_item:
                    print(deeper_item)
                else:
                    print(nested_item)
        else:
            print(each_item)"""

#遞迴比較快
def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
