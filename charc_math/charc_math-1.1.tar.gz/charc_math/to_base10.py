"""
    An inverse to to_base(n, b) -- list -> num
    @arg l  A list with the coeffecients in the exansion
            using powers of b
    @arg b  Base
    @ret    Integer in base 10
"""

# Code:
def to_base10(l, b):
    """
    An inverse to to_base(n, b) -- list -> num
    @arg l  A list with the coeffecients in the exansion
            using powers of b
    @arg b  Base
    @ret    Integer in base 10
    """
    ret = 0
    m = 1
    while len(l) != 0:
        ret += l.pop() * m
        m *= b
    return ret


# Bugs:
