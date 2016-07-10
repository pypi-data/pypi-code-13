"""
    Will run both the isAP and isGP commands
    @arg l  The list to be checked
    @ret    'GP' or 'AP' in relevant case, else False
"""

import is_ap
import is_gp

# Code:
def is_seq(l):
    """
    Will run both the isAP and isGP commands
    @arg l  The list to be checked
    @ret    'GP' or 'AP' in relevant case, else False
    """
    if is_ap.is_ap(l):
        return 'AP'
    elif is_gp.is_gp(l):
        return 'GP'
    else:
        return False


# Bugs:
