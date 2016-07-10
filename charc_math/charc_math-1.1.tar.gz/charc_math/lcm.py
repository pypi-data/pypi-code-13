"""
    Recursive finding of the LCM of a list of numbers
    With base being division by GCD
    @arg *n Any amount of integers
    @ret    The lowest common multiple
"""
from gcd import gcd

# Code:
def lcm(*n):
    """
    Recursive finding of the LCM of a list of numbers
    With base being division by GCD
    @arg *n Any amount of integers
    @ret    The lowest common multiple
    """
    l = list(n)
    if len(l) == 0:
        return 1
    elif len(l) == 1:
        return abs(l.pop())
    a = l.pop()
    b = l.pop()
    g = gcd(a, b)
    if len(l) == 0:
        return abs(a*b // g)
    else:
        l.insert(0, a*b // g)
        return abs(lcm(*l))


# Bugs:
# TODO Plans to make the recursion faster to somehow make it so
# we only calculate it for numbers which don't completely devide the
# other.

