"""
    Checks all numbers up to n to see if they are prime
    @arg n  The number to check up to
    @ret    A list of primes <= n
"""

# Code:
def primes(n):
    """
    Checks all numbers up to n to see if they are prime
    @arg n  The number to check up to
    @ret    A list of primes <= n
    """
    ret = []
    if n < 2:
        return []
    elif n == 2:
        return [2]
    else:
        ret.append(2)
        for i in range(3, n + 1, 2):# change to n if < n wanted
            for p in ret:
                if i % p == 0:
                    break
            else:
                ret.append(i)
    return ret


# Bugs:
