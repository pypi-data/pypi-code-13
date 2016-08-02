"""
学习Head First的第一二章练习
"""


# def print_lol(the_list):
#     """
#     递归打印嵌套数组
#     """
#     for item in the_list:
#         if isinstance(item, list):
#             print_lol(item)
#         else:
#             print(item)


def print_lol(the_list, level=0):
    """
    递归打印嵌套数组。带R缩进格式。
    """
    for item in the_list:
        if isinstance(item, list):
            level_inner = level + 1
            print_lol(item, level_inner)
        else:
            for i in range(level - 1):
                print("\t", end='')
            print(item)

# movies = ["Titanic", 2000, ["District", ["Euro", "American"]], ["Actor", ['Jack', 'Rose']]]

# print_lol(movies, 0)
