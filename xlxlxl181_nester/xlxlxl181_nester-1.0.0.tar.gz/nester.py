"""
    print xl test list
"""

def print_lol(cast):
    """
        print print_lol function
    """

    for i in cast:
        if (isinstance(i,list)):
            print_lol(i)
        else:
            print(i)
