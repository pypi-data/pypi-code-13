# Returns the previous prime after
# A specified number

import is_prime

def previous_prime(n):
    for i in range(n-1, 2, -1): #Descending list from n-1 to 1 in increments of -1.

        if is_prime.is_prime(i) == False: # If not prime, continue the search
            continue

        else: # If this condition is reached, none of the numbers below are prime
            return i

