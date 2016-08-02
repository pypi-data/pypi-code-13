"""This is the "nester.py" module, and it provides one function called print_lol() which prints lists that may or may not include nested lists."""
#i am a python learner who is following the tutorial of Head First Python
def print_lol(the_list, level):
    """This function takes a positional arguments called "the_list", which is any Python list. Each data item in the provided list is printed to the screen on its own line."""
    #version 1.1.0, indentation is added
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level + 1)
        else:
            for num in range(level):
                print("\t", end = '')
            print(each_item)
