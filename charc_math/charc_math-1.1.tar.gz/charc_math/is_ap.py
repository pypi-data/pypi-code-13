"""
    Calculates the common differences and checks if they are the same
        to find if the list is an arithmetic progression.
    @arg l    The list to check
    @arg eps  The accuracy to which we check (1e-15 by default)
    @ret      Boolean
"""

# Code:
def is_ap(l, eps=1e-15):
    """
    Calculates the common differences and checks if they are the same
        to find if the list is an arithmetic progression.
    @arg l    The list to check
    @arg eps  The accuracy to which we check (1e-15 by default)
    @ret      Boolean
    """
    # Edge Cases
    if len(l) < 2:
        return True
    # Common difference
    cdi = [l[i+1]-l[i] for i in range(len(l)-1)]
    # Common common difference
    ccd = [cdi[i+1]-cdi[i] for i in range(len(l)-2)]
    # Ideally ccd would be a sequence of 0s
    for elt in ccd:
        if abs(elt) >= eps:
            return False
    return True

# Bugs:
# Accuracy is still a problem since it is possible for something to
# be flagged falsely
# Vary the epsilon in this case.
