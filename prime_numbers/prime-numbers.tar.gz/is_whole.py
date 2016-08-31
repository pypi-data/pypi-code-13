# A function to determine weather
# a number is whole or not.
# Used as a guard for other functions
# Not specifically designed for use by
# end user of module

def is_whole(n):
    if n % 1 == 0:
        return True
    else:
        return False
