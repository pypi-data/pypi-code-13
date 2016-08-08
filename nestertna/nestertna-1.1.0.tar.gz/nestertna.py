""" This is my firt  module python"""

movies=['teste1','gran torinao', ['hard to die','goonies',['sub','adding more tabls']]]
def print_lol(the_list, level):
    """Recursive list iteration"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,level+1)
        else:
            for tab in range(level):
                print("\t", end='')
            print(each_item)


if __name__ == '__main__':
   print_lol(movies,1)