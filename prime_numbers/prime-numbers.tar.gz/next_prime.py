# Returns the next prime after
# A specified number

import is_prime


def next_prime(n):
    # Generate every number bigger than n
    for i in range(n + 1, 10000):

        if is_prime.is_prime(i) == False:
            continue

        else:
            return i
