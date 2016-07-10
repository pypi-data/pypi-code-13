"""
    Sets the file up to the way I like it.
    @ret    The file to be written to.
"""
import sys

# Code:
def start():
    """
    Sets the file up to the way I like it.
    @ret    The file to be written to.
    """
    return open(sys.argv[0][:-3] + 'Results.txt', 'wb')


# Bugs:
