"""
Recursive finding of the gcd or hcf of a list of numbers
@arg *n Any amount of integers
@ret    The greatest common divisor
"""

# Code:
def gcd(*n):
    """
    Recursive finding of the gcd or hcf of a list of numbers
    @arg *n Any amount of integers
    @ret    The greatest common divisor
    """
    l = list(n)
    if len(l) == 0: # len = 0, gcd of no numbers!
        return 1
    elif len(l) == 1: # len = 1, gcd(a) = a
        return l.pop()
    a = l.pop()
    b = l.pop()
    while b:
        a, b = b, a % b
    if len(l) == 0 or abs(a) == 1:
        return abs(a)
    else:
        l.insert(0, abs(a))
        return gcd(*l)


# Bugs:
