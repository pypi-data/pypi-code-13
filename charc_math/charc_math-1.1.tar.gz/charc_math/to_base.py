"""
    Will convert any interger from base 10 to base b
    @arg n  The number to convert
    @arg b  The base to convert n to
    @ret    Coeff from expansion base b
            -- a_i from n = Sum (a_i) b^i
"""

# Code:
def to_base(n, b):
    """
    Will convert any interger from base 10 to base b
    @arg n  The number to convert
    @arg b  The base to convert n to
    @ret    Coeff from expansion base b
            -- a_i from n = Sum (a_i) b^i
    """
    if n == 0:
        return [0]
    ret = []
    while n:
        ret.insert(0, n % b)
        n /= b
    return ret


# Bugs:
