"""
    Checks if a number is prime
    @arg n  The number we check
    @ret    Boolean
"""
import math as m

# Code:
def is_prime(n):
    """
    Checks if a number is prime
    @arg n  The number we check
    @ret    Boolean
    """
    if n < 2:
        return False
    elif n == 2:
        return True
    elif (n % 2) == 0:
        return False
    else:
        for i in range(3, int(m.sqrt(n)) + 1, 2):
            if (n % i) == 0:
                return False
    return True


# Bugs:
