"""
Module for recursively printing the contents of nested lists
"""
def printsubitem (item, level=0):
        """
        If the item is a list, print it's components recursively
        """
        if not isinstance(item, list):
			for tab_stop in range(level):
				print("\t", end='')
            print(item)
        else:
            for subitem in item:
                printsubitem(subitem, level + 1)
