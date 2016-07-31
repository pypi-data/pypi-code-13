"""
学习Head First的第一二章练习
"""


def print_lol(the_list):
    """
    递归打印嵌套数组
    """
    for item in the_list:
        if isinstance(item, list):
            print_lol(item)
        else:
            print(item)

# movies = ["Titanic", 2000, ["Actor", ['Jack', 'Rose']]]

# print_lol(movies)
