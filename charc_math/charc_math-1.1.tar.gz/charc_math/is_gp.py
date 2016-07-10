"""
    Calculates the log of the sequence and checks if this is an AP
    @arg l  The list to check
    @ret    Boolean
"""

# Code:
def is_gp(l):
    """
    Calculates the log of the sequence and checks if this is an AP
    @arg l  The list to check
    @ret    Boolean
    """
    # Edge Cases
    if len(l) < 2:
        return True
    # Common Ratio Testing
    for i in range(len(l) - 2):
        if l[i] * l[i + 2] != l[i + 1] ** 2:
            return False
    # Unless ratio is 0
    for i in range(len(l) - 1):
        if l[i] == 0 and l[i + 1] != 0:
            return False
    return True

# Bugs:
# Accuracy - is_gp([1.2**i for i in range(4)]) = False as 1.2**3 is
# too small.
# A solution using log10 and is_ap can be used for the very small solutions, but this is to be checked.
