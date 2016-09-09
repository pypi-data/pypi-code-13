# -*- coding: utf-8 -*-

""" Module for miscellaneous arithmetic calculation
"""

__all__ = ('gcd', 'lcm', 'bezout', 'modulo_inv', 'chinese_reminder', 
           'gene_pseudo_primes', 'is_prime', 'next_prime', 'prime_factorization', 
           'divisors', 'phi', 'moebius', 'to_base', 'frobenius')

__version__ = '0.0.1'
__copyright__ = ""
__author__ = "jm allard"
__email__ = "jma412@gmail.com (swap digits 4 and 2)"



def _gcd2(a, b):
    """ Calculates the greatest common divisor (gcd) of a and b

    Private function, do not use. Use gcd instead.
    Implements Euclide's algorithm.
    If a and b are both 0, returns 0

    :type a:    int >= 0
    :type b:    int >= 0

    :return:       gcd(a, b)
    :rtype:        int

    :Example:

    >>> _gcd2(0, 0)
    0
    >>> _gcd2(11, 0)
    11
    >>> _gcd2(0, 7)
    7
    >>> _gcd2(7**5 * 3**4, 7**2 * 3**6)
    3969
    """

    if b == 0: return a

    while True:              # gcd(a, b) = gcd(b, r) with r = a % b, 0 <= r < b
                             # repeat until r==0. returns gcd(b, 0) ->  b
        r = a % b

        if r == 0: return b

        a, b = b, r


def gcd(*arg):
    """ Calculates the greatest common divisor (gcd) of a list of int
        Usage: gcd(15, 20, 10) -> 5

    Calculation is done 2 par 2 using _gcd2
    Return 0 if arg contains only zeros

    :type arg: iterable of int
    :return:   gcd(a, b, c, ...)
    :rtype:    int

    :Example:

    >>> gcd()
    Traceback (most recent call last):
    ...
    ValueError: Empty list of arguments

    >>> gcd(7, 14.0)
    Traceback (most recent call last):
    ...
    ValueError: Arguments shall be integers

    >>> gcd(0,0,0,0)
    0
    >>> gcd(11)
    11
    >>> gcd(0, 7)
    7
    >>> gcd(-15, -20)
    5
    >>> gcd(7**5 * 3**4, 7**2 * 3**6, -7**2 * 3**3)
    1323
    """

    if not arg:
        raise ValueError("Empty list of arguments")

    if not all(isinstance(n, int) for n in arg):
        raise ValueError("Arguments shall be integers")

    gcd_tmp = 0

    for n in arg:    

        gcd_tmp = _gcd2(gcd_tmp, abs(n))

    return gcd_tmp


def _lcm2(a, b):
    """ Calculates the least common multiple (lcm) of a and b

    Private function, do not use. Use lcm instead
    a and b shall not be both 0
    Use the relationship: gcd(a, b) * lcm(a, b) = a * b

    :type a:    int >= 0
    :type b:    int >= 0

    :return:       lcm(a, b)
    :rtype:        int

    :Example:

    >>> _lcm2(0, 0)
    Traceback (most recent call last):
    ...
    ZeroDivisionError: integer division or modulo by zero

    >>> _lcm2(0, 67)
    0
    >>> _lcm2(77, 0)
    0
    >>> _lcm2(7**4 * 11**3, 7**2 * 11**5)
    386683451
    """

    return a*b // _gcd2(a, b)


def lcm(*arg):
    """ Calculates the least common multiple (lcm) of a list of int
        Usage: lcm(6, 9, 12) -> 36 

    Calculation is done 2 par 2 using _lcm2
    Return 0 if arg contains at least one zero

    :type arg: iterable of int
    :return:   lcm(a, b, c, ...)
    :rtype:    int

    :Example:

    >>> lcm()
    Traceback (most recent call last):
    ...
    ValueError: Empty list of arguments
    >>> lcm(8,1,0,9)
    0
    >>> lcm(11)
    11
    >>> lcm(7, -7)
    7
    >>> lcm(-7**5 * 3**4, 7**2 * 3**6, 7**2 * 3**3)
    12252303
    """

    if not arg:
        raise ValueError("Empty list of arguments")

    if not all(isinstance(n, int) for n in arg):
        assert ValueError("Arguments shall be integers")

    if not all(arg): return 0

    lcm_tmp = 1

    for n in arg:

        lcm_tmp = _lcm2(lcm_tmp, abs(n))

    return lcm_tmp


def bezout(a, b):
    """ bezout function finds a particular integer solution
    (u, v) to the Diophantine equation a.u + b.v = gcd(a, b)
    Returns (u, v, gcd(a, b))
    Usage: bezout(5, 8) -> (-3, 2, 1)   
    
    Implements extended Euclide's algorithm.

    :type a:    int 
    :type b:    int (a and b not both 0)

    :return:  (u, v, gcd(a,b))
    :rtype:   int x3

    :Example:
    
    >>> bezout(120, 23); bezout(-120, 23); bezout(-120, -23); bezout(120, -23)
    (-9, 47, 1)
    (9, 47, 1)
    (9, -47, 1)
    (-9, -47, 1)
    >>> bezout(1, 10); bezout(1, -10); bezout(10, 1); bezout(-10, 1)
    (1, 0, 1)
    (1, 0, 1)
    (0, 1, 1)
    (0, 1, 1)
    >>> bezout(-1, 10); bezout(-1, -10); bezout(10, -1); bezout(-10, -1)
    (-1, 0, 1)
    (-1, 0, 1)
    (0, -1, 1)
    (0, -1, 1)
    >>> bezout(0, 10); bezout(0, -10); bezout(-10, 0); bezout(10, 0)
    (0, 1, 10)
    (0, -1, 10)
    (-1, 0, 10)
    (1, 0, 10)
    >>> bezout(1, 0); bezout(-1, 0)
    (1, 0, 1)
    (-1, 0, 1)
    >>> bezout(1, 1); bezout(-1, 1); bezout(1, -1); bezout(-1, -1)
    (0, 1, 1)
    (0, 1, 1)
    (0, -1, 1)
    (0, -1, 1)
    >>> def test_bezout(a, b):
    ...     u, v, g = bezout(a, b)
    ...     return a*u+b*v==g and g==gcd(a, b)
    >>> all(test_bezout(a, b) \
    for a in range(-1000, 2000, 99) for b in range(-1000, 1000, 51))
    True
    >>> bezout(0, 0)
    Traceback (most recent call last):
    ...
    ValueError: a and b shall not be both 0
    """
    
    if a == 0  and b == 0:
        raise ValueError("a and b shall not be both 0")
    
    sign_a = 1             # Do the calculation with abs(a) and abs(b)
    if a < 0:              # and change the sign of solutions (u, v)
        a = -a             # at the end if a or b are negative
        sign_a = -1
    
    sign_b = 1;
    if b < 0:
        b = -b
        sign_b = -1

    if a == 0: return 0, sign_b, b  # 0*u+b*v = gcd(0, b) = abs(b) -> 0, sign_b, b   
    if b == 0: return sign_a, 0, a  # a*u+0*b = gcd(a, 0) = abs(a) -> sign_a, 0, a
        
    u1, v1 = 1, 0                 # a = 1*a + 0*b  
    u2, v2 = 0, 1                 # b = 0*a + 1*b

    while True:                   # r(n-1) = u1*a + v1*b
                                  # r(n)   = u2*a + v2*b
                                  
        q, r = divmod(a, b)       # a = b*q + r

        if r == 0:
            return sign_a * u2, sign_b * v2, b
        
        u1, v1, u2, v2 = u2, v2, u1-q*u2, v1-q*v2
        a, b = b, r


def modulo_inv(a, b):
    """ This function provides the inverse of a modulo b
        (b >= 2 and gcd(a, b) = 1)
        Usage: modulo_inv(4, 11) -> 3   (4*3 = 12 = 1 (mod 11)
        

    :param a: The number to be inverted
    :type a: int

    :param b: The modulo
    :type b: int >= 2, gcd(a,b) shall be 1

    :return: The inverse of a (mod b)
    :rtype: int, 1 <= modulo_inv(a, b) < b

    :Example:

    >>> for a in range(-1000, 1000, 11):
    ...     for b in range(2, 100, 7):
    ...         if not gcd(a, b)==1: continue
    ...         inv = modulo_inv(a, b)
    ...         assert 1 <= inv < b and (a*inv) % b == 1
    
    """
    
    if not (gcd(a, b)==1 and b>=2):
        raise ValueError("b < 2 or gcd of a and b is not 1")

    u, v, g = bezout(a, b)

    return u % b         # % b to get a number between 0 and b-1 (included)


def chinese_reminder(r, m):
    """ Solves the modular system (x is the integer unknow):   
    x = r1 mod m1
    x = r2 mod m2       Usage: chinese_reminder((3, 4, 5), (17, 11, 6)) -> 785
    ...                 for r1=3, r2=4, r3=5 and m1=17, m2=11, m3=6   -> x=785
    x = r_n mod m_n   
    
    r1, r2, ..., r_n, m1, m2, ..., m_n are some parameters
    m1, m2, ..., m_n shall be >= 2 and primes 2 per 2
    r=(r1, r2, ..., r_n) and m=(m1, m2, ..., m_n)

    :param r: The rests r1, r2, ... r_n
    :type r: An iterable of int (r1, r2, ... r_n)

    :param m: The modulo m1, m2, ..., m_n
    :type m: An iterable of int >= 1 (m1, m2, ..., m_n)

    :Example:

    >>> chinese_reminder((3, 4, 5), (17, 11, 6))
    785
    >>> chinese_reminder((2, 3, 2), (3, 5, 7))
    23
    >>> chinese_reminder((3, 5), (4, 9))
    23
    >>> chinese_reminder((2, 3, 2, 8), (12, 5, 7, 121))
    32678
    >>> chinese_reminder((3, 0), (2, 9))
    9
    """

    if not all(mi>=2 for mi in m):
        raise ValueError("Modulos shall be integers >= 2")
    
    for i in range(len(m)-1):    #  checks that modulo mi are prime 2 per 2
        for j in range(i+1, len(m)):
            if not gcd(m[i], m[j])==1:
                raise ValueError("modulo shall be prime 2 per 2")
    
    prod=1                 # prod = m1 * m2 * m3 * ...
    for mi in m:
        prod=prod*mi

    M=[]                   # M=[m2*m3*m4..., m1*m3*m4*..., m1*m2*m4*..., ...]
    for mi in m:
        M.append(prod // mi)

    U=[]
    for Mi, mi in zip(M, m):  # calculates all Mi inverse mod mi
        U.append(modulo_inv(Mi, mi))

    return sum(Ui*Mi*ri for Ui, Mi, ri in zip(U, M, r)) % prod

    
def to_base(n, base=16, use_AF=True, sep=''):
    """Convert integer n from base 10 to base 'base'. Return a string.
    If use_AF is True, then characters A, ..., F are used instead
    of 10, ..., 15 when base is between 11 to 16.
    sep is a separator between digits after conversion. If sep is ''
    then digits are left justified with 0 if needed

    :param n:      The number to be converted
    :type n:       int >= 0

    :param base:   The base after conversion
    :type base:    int >= 2

    :param use_AF: Chars A-F used when True for base between 11 to 16
    :type use_AF:  Boolean

    :param sep:    A one char (or '') separator between digit after conversion
    :type sep:     str  (1 char or empty string '')

    :return:       nrepresentation in base 'base'
    :rtype:        str

    :Example:

    >>> to_base(0, base=9)
    '0'
    >>> to_base(167, base=2)
    '10100111'
    >>> to_base(351, base=17)
    '010311'
    >>> to_base(351, base=17, sep='.')
    '1.3.11'
    >>> to_base(347, base=12, use_AF=True)
    '24B'
    >>> to_base(65000, base=16, use_AF=True)
    'FDE8'
    >>> to_base(347, base=12, use_AF=True, sep='.')
    '2.4.B'
    >>> to_base(347, base=12, use_AF=False)
    '020411'
    >>> to_base(347, base=12, use_AF=False, sep='.')
    '2.4.11'
    """

    ## Checking function's parameters

    n=int(n)
    if n < 0:
        raise ValueError("Negative numbers not supported")

    base = int(base)
    if base < 2:
        raise ValueError("Base shall be at least 2")

    use_AF = bool(use_AF)

    sep = str(sep)
    if len(sep) > 1:
        raise ValueError("sep shall be a single char or an empty string")

    # Start conversion

    conv = ''
    mapping = "0123456789ABCDEF"
    l_base = len(str(base))

    if n== 0:
        return '0'

    first = True

    while n != 0:

        sep2 = '' if first else sep
        first = False

        n, remains = divmod(n, base)

        if base <= 16 and use_AF:
            conv = mapping[remains] + sep2 + conv

        elif sep != "":
            conv = str(remains) + sep2 + conv

        else:
            conv = str(remains).rjust(l_base, '0') + conv

    return conv


def gene_seq(n):
    """ when parameter n is 0, this function  provides a generator which
        yields 4, 2, 4, 2, 4, 6, 2, 6 and again 4, 2, 4, 2, 4, 6, 2, 6
        and again endless.

        If n is not 0, start occurs at sequence[n] instead
        (sequence = [4, 2, 4, 2, 4, 6, 2, 6])

        :Exemple:

        >>> seq = gene_seq(0)
        >>> [next(seq) for i in range(20)]
        [4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2]
        >>> seq = gene_seq(5)
        >>> [next(seq) for i in range(20)]
        [6, 2, 6, 4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 4, 6, 2, 6, 4]
          
    """
    
    sequence = [4, 2, 4, 2, 4, 6, 2, 6]
    
    for i in range(n):
        sequence.append(sequence.pop(0))
        
    while True:
        yield from sequence


def gene_pseudo_primes():
    """ A function which provides a generator which yields 2, 3, 5
    and then all integers non multiple of 2, 3, 5, endless

    :Exemple:

    >>> divisors = gene_pseudo_primes()
    >>> [next(divisors) for n in range(20)]
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67]

    """

    seq = gene_seq(0)        
    div = 7
    
    yield from (2, 3, 5)

    while True:
        yield div
        div += next(seq)
        

from math import sqrt


def is_prime(n):
    """ Returns True if argument 'n' is a prime number, else False

    :Example:

    >>> is_prime(0)
    False
    >>> is_prime(1)
    False
    >>> is_prime(2)
    True

    >>> [n for n in range(60) if is_prime(n)]
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]

    >>> import hashlib
    >>> hasher = hashlib.md5()
    >>> for p in [n for n in range(1000) if is_prime(n)]:
    ...     hasher.update(p.to_bytes(p.bit_length() // 8 + 1, 'big'))
    >>> hasher.hexdigest()
    '079bc030916d4260a7d5c392dcb8b967'

    >>> is_prime(-4)
    Traceback (most recent call last):
    ...
    ValueError: Argument shall be a positive integer

    >>> is_prime(7.9)
    Traceback (most recent call last):
    ...
    ValueError: Argument shall be a positive integer

    """

    if not isinstance(n, int) or  n < 0:
        raise ValueError("Argument shall be a positive integer")

    if n == 0 or n == 1:
        return False

    divisors = gene_pseudo_primes()
    stop = sqrt(n)

    div = next(divisors)

    while div <= stop:     # test pseudo prime divisors up to square root

        if n % div == 0:
            return False

        div = next(divisors)

    return True


offset = ((1, 7), (0, 7),
          (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0),
          (3, 1), (2, 1), (1, 1), (0, 1),
          (1, 2), (0, 2),
          (3, 3), (2, 3), (1, 3), (0, 3),
          (1, 4), (0, 4),
          (3, 5), (2, 5), (1, 5), (0, 5),
          (5, 6), (4, 6), (3, 6), (2, 6), (1, 6), (0, 6)
          )

def next_prime(n):
    """ This function provides the first prime greater or equal to n
        (n >= 0)

    :Exemple:

    >>> next_prime(0)
    2
    >>> next_prime(7)
    7
    >>> next_prime(20)
    23
    >>> next_prime(9000012)
    9000041
    >>> next_prime(-4)
    Traceback (most recent call last):
    ...
    ValueError: n shall be a positive integer
    
    To get all primes between 1000 and 2000
    >>> n = 1000; lst = []
    >>> while n <= 2000:
    ...     p = next_prime(n)
    ...     lst.append(p)
    ...     n = p + 1
    >>> lst # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061,
     1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123,
     ...,
     1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931,
     1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003]
    >>> len(lst)
    136
   
    """

    if not isinstance(n, int) or n < 0:
        raise ValueError("n shall be a positive integer")
    
    if n <= 5:

        if n <= 2:
            return 2    
        if n == 3:
            return 3
        if n == 4 or n == 5:
            return 5
    
    rmd = n % 30
    n = n + offset[rmd][0]  # first nber >= n and non multiple with 2, 3, 5 
    rot = offset[rmd][1]    
    seq = gene_seq(rot)     # synchronize sequence 4, 2, 4, 2, 4, 6, 2, 6
                            #                            | eg start here
    while True:

        if is_prime(n):
            return n

        n = n + next(seq)


def prime_factorization(n, frmt='tuple'):
    """ Provides the prime factorization of n (n >= 2)
    if frmt is set to 'str', a string is provided, eg '3**2 * 7**4 * 13'
    if frmt is set to 'tuple', a tuple is provided, eg ((3, 2), (7, 4), (13, 1))

    :Exemple:

    >>> prime_factorization(280917, frmt='str')
    '3**2 * 7**4 * 13'
    >>> prime_factorization(280917)
    ((3, 2), (7, 4), (13, 1))
    >>> prime_factorization(2, frmt='str')
    '2'
    >>> prime_factorization(2)
    ((2, 1),)

    >>> for i in range(2, 10000):
    ...     j = eval(prime_factorization(i, frmt='str'))
    ...     if i != j:
    ...         print(i, ' != ', j)

    >>> prime_factorization(1)
    Traceback (most recent call last):
    ...    
    ValueError: nber shall be an integer >= 2

    >>> prime_factorization(4, frmt='foo')
    Traceback (most recent call last):
    ...
    ValueError: frmt shall be 'tuple' or 'str'
    
    """

    nber = n

    divisors = gene_pseudo_primes()  # 2, 3, 5 then all non multiple of 2, 3, 5
    div = next(divisors)
    factors = []
    stop = sqrt(nber)

    ## checking inputs
    
    if not (isinstance(nber, int) and nber >= 2):
        raise ValueError("nber shall be an integer >= 2")

    if not (frmt == 'tuple' or frmt == 'str'):
        raise ValueError("frmt shall be 'tuple' or 'str'")

        
    ## main calculation
    
    while True:

        exp = 0

        while nber % div == 0:            # found div**exp as a factor
            nber //= div
            exp += 1

        if exp != 0:
            factors.append((div, exp))    # store found factor and updates
            stop = sqrt(nber)             # the search bound
            
        if div > stop:                    # a single prime with no exponent
            if nber != 1:                 # is still here
                factors.append((nber, 1))
            break

        div = next(divisors)              # possibly primes are run through

    ## format and provide output        

    if frmt == 'tuple':          ## provides a tuple eg ((3, 2), (7, 4), (13, 1))
        return tuple(factors)
    else:                        ## processing to return a string '3**2 * 7**4 * 13'
        return (''.
                join([str(tpl[0]) + "**" + str(tpl[1]) + " * " for tpl in factors]).
                replace('**1 ', ' ').
                rstrip(' *')
                )


def divisors(n):
    """ This function returns the list of the positive divisors
        of n including 1 and n. (n > 0)

    :Example:
    
    >>> divisors(1)
    [1]
    >>> divisors(45)
    [1, 3, 9, 5, 15, 45]
    >>> divisors(645)
    [1, 3, 5, 15, 43, 129, 215, 645]
    >>> all(n%d==0 for n in range(1000, 2000) for d in divisors(n) )
    True
    >>> divisors(0)
    Traceback (most recent call last):
    ...
    ValueError: n shall be > 0
       
    """

    if n <= 0: raise ValueError("n shall be > 0")

    if n==1: return [1]  # prime_factorization() fails when n=1

    # n = p1**m1 * p2**m2 + ...   (prime factorization of n)
    # factors = ((p1, m1), (p2, m2), ...)
    
    factors = prime_factorization(n)

    # P = (p1, p2, ...) and M = (m1, m2, ...)
    
    P, M = zip(*factors)  
    E = [0 for _ in M]

    def nxt():                  # "Increments" E 
                                # digit E(i) goes from 0 to M(i)
        for i in range(len(E)):          
            if E[i] == M[i]:
                E[i] = 0
                if i == len(E)-1:
                    return True
            else:
                E[i] += 1                
                return False

    divisors_list = []

    end = False
    
    while not end:

        prod = 1               # Calculation of p1**e1 * p2**e2 * ...
        for p, e in zip(P, E): # All n divisors are found when e1, e2, ...
            prod *= p**e       # goes from 0 to m1, 0 to m2, ...
            
        divisors_list.append(prod)

        end = nxt()

    return divisors_list        


def phi(n):
    """ Euler indicator function
        phi(n) provides the number of integers <= n and prime
        with n. (n shall be > 0)       

    >>> for n in range(1, 100): # doctest: +NORMALIZE_WHITESPACE
    ...    print(phi(n))  
            1   1   2   2   4   2   6   4   6
	4   10	4   12	6   8	8   16	6   18
	8   12	10  22	8   20	12  18	12  28
	8   30	16  20	16  24	12  36	18  24
	16  40	12  42	20  24	22  46	16  42
	20  32	24  52	18  40	24  36	28  58
	16  60	30  36	32  48	20  66	32  44
	24  70	24  72	36  40	36  60	24  78
	32  54	40  82	24  64	42  56	40  88
	24  72	44  60	46  72	32  96	42  60

    >>> phi(75409883)
    75409882
    >>> phi(0)
    Traceback (most recent call last):
    ...
    ValueError: n shall be > 0
    """

    if n <= 0: raise ValueError("n shall be > 0")
    
    if n==1: return 1

    # n = p1**m1 * p2**m2 *
    # factors = ((p1, m1), (p2, m2), ...)
    # phi(n) = (p1-1)*p1**(m1-1) * (p2-1)*p2**(m2-1) * ...
    
    product = 1
    for factors in prime_factorization(n):
        product *= (factors[0]-1)*factors[0]**(factors[1]-1)

    return product


def moebius(n):
    """ moebius function is defined from N* to {-1, 0, 1}
        - moebius(1) = 1, else
        - if n is a multiple of a square then moebius(n) = 0, else
        - if n if the product of an even number of primes, moebius(n) = 1, else
        - n is the product of an odd number of primes, moebius(n) = -1

        :Example:

        >>> moebius(1)
        1

        >>> for n in range(1, 31):  # doctest: +NORMALIZE_WHITESPACE
        ...     print(moebius(n), end=" ")
        1 -1 -1 0 -1 1 -1 0 0 1 -1 0 -1 1 1 0 -1 0 -1 0 1 1 -1 0 0 1 0 0 -1 -1

        >>> L = []
        >>> for n in range(1, 201):  # doctest: +NORMALIZE_WHITESPACE
	...     sum = 0; sum2 = 0
	...     for d in divisors(n):
	...	    sum += moebius(d)
	...         sum2 += moebius(d) * n // d
	...     L.append(phi(n)==sum2)
	...     print(sum, end="")
	...     if n%40==0: print()
	1000000000000000000000000000000000000000
	0000000000000000000000000000000000000000
	0000000000000000000000000000000000000000
	0000000000000000000000000000000000000000
	0000000000000000000000000000000000000000	
	>>> all(L)
	True

        >>> moebius(-5) 
        Traceback (most recent call last):
        ...
        ValueError: Parameter n shall be an integer >= 1
    """

    if not (isinstance(n, int) and n >= 1):
        raise ValueError("Parameter n shall be an integer >= 1")
        
            
    if n == 1:
        return 1

    # n = p1**m1 * p2**m2 *
    # factorization = ((p1, m1), (p2, m2), ...)
    
    factorization = prime_factorization(n)

    for factor in factorization: 
        if factor[1] >= 2:        # a square is found
            return 0

    if len(factorization) % 2 == 0:
        return 1                  # even number of primes
    else:
        return -1                 # odd number of primes
    

def frobenius(*A, n=None):
    """ frobenius function copes with equation "a1.x1 + a2.x2 + .. + ap.xp = n"
    where (a1, a2 ...) are the coefficients (at least 2 integers >= 2, with
    GCD(a1, a2, ...) == 1), (x1, x2 ...) are the unknows (integers >= 0) and
    n a parameter (integer >= 0).

    ## If n is not provided or n is None, function frobenius provides the
    greatest n denoted g(a1, a2 ...) for which the equation has no integer
    solution, nri the Number of Non Representable Integers (n for which the
    equation has no solution), and nri_list the list of these integers.
    frobenius is invoked like that: g, nri, nri_list = frobenius(a1, a2, ...)

    :Example:

    >>> g, nri, nri_list = frobenius(6, 9, 20)
    >>> g
    43
    >>> nri
    22
    >>> nri_list # doctest: +NORMALIZE_WHITESPACE
    (1, 2, 3, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 22, 23, 25, 28, 31, 34, 37, 43)

    >>> g, nri, nri_list = frobenius(31, 41)
    >>> g == 31*41 - 31 - 41 == 1199
    True
    >>> nri == (31-1)*(41-1)//2 ==  600
    True
    >>> nri_list # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
    ...
    922, 931, 932, 941, 942, 951, 952, 953, 962, 963, 972, 973, 982, 983, 993, 994,
    1003, 1004, 1013, 1014, 1024, 1034, 1035, 1044, 1045, 1055, 1065, 1075, 1076,
    1086, 1096, 1106, 1117, 1127, 1137, 1158, 1168, 1199)

    >>> frobenius(17, 18, 31, 32) # doctest: +NORMALIZE_WHITESPACE
    (109, 56, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21,
    22, 23, 24, 25, 26, 27, 28, 29, 30, 33, 37, 38, 39, 40, 41, 42, 43, 44, 45,
    46, 47, 55, 56, 57, 58, 59, 60, 61, 73, 74, 75, 76, 77, 78, 91, 92, 109))
    
    ## If n is provided, function frobenius yields all solutions to equation
    "a1.x1 + a2.x2 + .. + ap.xp = n", if any.

    :Example:

    >>> frobenius(11, 25, 47, n=342)  # five solutions
    ((22, 4, 0), (20, 3, 1), (18, 2, 2), (16, 1, 3), (14, 0, 4))
    
    >>> frobenius(17, 97, 51, n=577)  # no solution
    ()

    Some tests for bad inputs
    
    >>> frobenius(6.0, 7, 4)
    Traceback (most recent call last):
    ...
    ValueError: Coefficients shall be integers >= 2

    >>> frobenius(77, 1, 12, n=None)
    Traceback (most recent call last):
    ...
    ValueError: Coefficients shall be integers >= 2

    >>> frobenius(5, 88, 654, n=-5)
    Traceback (most recent call last):
    ...
    ValueError: Parameter n shall be a positive integer or None

    >>> frobenius(9, 33, 21)
    Traceback (most recent call last):
    ...
    ValueError: GCD of coefficients shall be 1
           
    """

    if not all([isinstance(a, int) and (a > 1) for a in A]):
        raise ValueError("Coefficients shall be integers >= 2")

    if not ((isinstance(n, int) and n >= 0) or n is None):
        raise ValueError("Parameter n shall be a positive integer or None")
    
    if gcd(*A) != 1:
        raise ValueError("GCD of coefficients shall be 1")

    def nxt():
        """ This function updates X to next value, and possibly updates M

            X is the list of variables x1, x2 ... of eq "a1.x1 +a2.x2 + ... = n"
            M is the list of max possible values for x1, x2 ..
            0 <= xi <= M(i)
            A is the list of coefficients a1, a2, ... of eq "a1.x1 +a2.x2 + ... = n"

            The function returns True when all X values have been scanned, else False
        """
                
        for i in range(len(X)):   # "increments" X, X[i] from 0 to M[i]
            if X[i] == M[i]:
                X[i] = 0
                if i == len(X)-1:
                    return True
            else:
                X[i] += 1
                for j in range(i):
                    M[j] = (n-sum(a*x for a, x in zip(A[i:], X[i:]))) // A[j] ## always >= 0
                    
                return False


    if n is None:  ## n not provided, search for g(a1, a2, ...), nri and nri_list
    
        n = 0               ## right member of equation "a1.x1 +a2.x2 + ... = n"
        successive_hit = 0
        previous_n_hit = -2 ## -2 because no successive hit wanted with n=0
        last_n_not_hit = 1
        nri = 0             ## Non Representable Integers (numbers "n" with no
                            ## solution to equation "a1.x1 +a2.x2 + ... = n"
        nri_list = []       ## List of all non representable integers
        list_n_hit = []     ## List of n for which a solution to equation has been found
                            ## multiple of already stored n are not stored again
        shortcut = 0

        while True:  ## "n" loop

            if any([n%d == 0 for d in list_n_hit]): ## is n a multiple of a previous found n
                                                    ## with a solution to equation ?
                if n == previous_n_hit + 1:          
                    successive_hit += 1
                else:
                    successive_hit = 1

                if successive_hit == min(A):  ## job finished
                    return last_n_not_hit, nri, tuple(nri_list)

                previous_n_hit = n
                n += 1
                shortcut += 1

                continue ## go to "n" loop              

            X = [0 for a in A]     ## variables x1, x2 ... of eq "a1.x1 +a2.x2 + ... = n"
            M = [n//a for a in A]  ## Max possible values of X coefficients

            while True:   ## "X" loop

                summation = sum([a*x for a, x in zip(A, X)])
                             
                if summation == n:    # A solution to "a1.x1 +a2.x2 + ... = n" has been found
                    
                    if n == previous_n_hit + 1:  ## looking for min(A) consecutive hits
                        successive_hit += 1
                    else:
                        successive_hit = 1

                    if successive_hit == min(A):  ## job finished
                        return last_n_not_hit, nri, tuple(nri_list)

                    previous_n_hit = n
                    
                    if n != 0:                    ## 0 excluded because these values
                        list_n_hit.append(n)      ## are used to test divisors of n
                    n += 1
                    
                    break  ## breaks "X" loop, so go to "n" loop

                else:
                    
                    end = nxt()  ## provides next X and possibly updates M

                    if end:      ## All X have been scanned, no solutions found
                        
                        last_n_not_hit = n
                        nri += 1
                        nri_list.append(last_n_not_hit)
                        n += 1
                        
                        break ## breaks "X" loop, so go to "n" loop
        

    else:  # n is provided, solve equation "a1.x1 +a2.x2 + ... = n"

        solutions = []
        X = [0 for a in A]
        M = [n//a for a in A]
        end = False

        while not end:

            if sum([a*x for a, x in zip(A, X)]) == n:
                solutions.append(tuple(X))
                
            end = nxt()

        return tuple(solutions)

                
## running doctest when module is executed

if __name__ == "__main__":
    import doctest
    doctest.testmod()
