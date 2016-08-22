"""This is the "SimonFirstNester.py" module and it provides one function called print_list()
    which prints lists that may or may not include nested lists."""


def print_list(the_list, level):
    """This function takes one positional argument called "the_list", which is any Python
        list(of - possibly - nested lists). Each data item in the provided list is
         (recursively) printed to the screen on it's own line. """
    for item in the_list:
        if isinstance(item, list):
            print_list(item, level+1)
        else:
			for step in range(level):
				print("\t", end = '')
            print(item)
