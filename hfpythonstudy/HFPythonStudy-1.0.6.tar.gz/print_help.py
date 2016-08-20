import sys

# sys.stdout 是标准输出
def print_lol(the_list, intent=False, level=0, out=sys.stdout):
    if isinstance(the_list, list):
        for each_item in the_list:
            if isinstance(each_item, list):
                print_lol(each_item, intent, level + 1, out)
            else:
                if intent:
                    # range创建指定数字的列表
                    for tab_stop in range(level):
                        print("\t", end='', file=out)
                print(each_item, file=out)
    else:
        print(the_list, file=out)
