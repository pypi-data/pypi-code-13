# Returns true or False
# Depending on weather the number is prime or not
#
# Usage:
# is_prime(n) where n is the number to determine primeness

import is_whole

def is_prime(n):
    if n <= 1 or is_whole.is_whole(n) == False:
        return False

    else:
        for i in range(2, n):
            if n % i == 0:
                return False

            if i == n - 1:
                return True
