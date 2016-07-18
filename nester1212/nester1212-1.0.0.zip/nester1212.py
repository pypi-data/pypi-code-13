def print_lol(the_list):
    """输入列表，输出元素"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
