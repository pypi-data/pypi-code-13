# Will generate a list of primes
# between n and m
#
# Usage
# primes_between(n, m) where n is the lower integer and m is the greater one
# if n > m function does not return a value

import is_prime

def primes_between(n, m):
    primes_list = []

    if n > m:
        raise ValueError('The first input number must be greater than the second')

    for i in range(n, m):  # Generate all numbers between (n + 1) and (m - 1)

        if i >= (m - 1): # The range (i) has reached m - 1
            if not is_prime.is_prime(m-1): # If (i OR m-1 - they're the same) is not prime, return the list and function is finished
                return primes_list

            if is_prime.is_prime(m-1) == True: # If m-1 is prime, add it to the list and return that
                primes_list.append(m-1)
                return(primes_list)

        if is_prime.is_prime(i) == False: # If the integer is not prime, continute to the next one
            continue

        if is_prime.is_prime(i) == True: # If the integer is prime, add it to the list and continue
            primes_list.append(i)        # We keep doing this until the value of m-1 is reached
            continue

# Will return the number of primes
# Between the inputs n and m

def number_between(n, m):
    return len(primes_between(n, m))