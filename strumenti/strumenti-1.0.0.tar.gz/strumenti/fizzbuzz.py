#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Fizzbuzz Module

Solve the fizz-buzz interview question.

Create a list of numbers from 1-100.
    - numbers divisible by 3 are replaced by "fizz"
    - numbers divisible by 5 are replaced by "buzz"
    - numbers divisible by 3 & 5 are replaced by "fizzbuzz"

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

import numpy as np


def fizz_buzz(min_n=1, max_n=100):
    """Solve the fizz-buzz interview question using a helper function.

    :param int min_n: minimum number to evaluate
    :param int max_n: maximum number to evaluate
    :returns: numbers from 1 to max_n with multiples of 3 replaced by "fizz", \
        multiples of 5 replaced by "buzz", and multiples of 3 & 5 replaced by \
        "fizzbuzz"
    :rtype: list
    """
    def evaluate(number):
            if all([number % 3 == 0, number % 5 == 0]):
                return 'fizzbuzz'
            elif number % 3 == 0:
                return 'fizz'
            elif number % 5 == 0:
                return 'buzz'
            else:
                return str(number)

    return [evaluate(n) for n in range(min_n, max_n + 1)]


def fizz_buzz_np(min_n=1, max_n=100):
    """Solve the fizz-buzz interview question using numpy arrays.

    :param int min_n: minimum number to evaluate
    :param int max_n: maximum number to evaluate
    :returns: numbers from 1 to max_n with multiples of 3 replaced by "fizz", \
        multiples of 5 replaced by "buzz", and multiples of 3 & 5 replaced by \
        "fizzbuzz"
    :rtype: recarray
    """
    init_range = range(int(min_n), int(max_n) + 1)
    str_range = [str(x) for x in init_range]
    str_dtype = '{}'.format(max(len(str(max_n)), 8))

    arr = np.empty(int(max_n), dtype=[('int', 'i4'),
                                      ('str', 'S{}'.format(str_dtype))])
    arr['int'] = init_range
    arr['str'] = str_range

    mask_fizz = arr['int'] % 3 == 0
    mask_buzz = arr['int'] % 5 == 0
    mask_fizzbuzz = np.all((mask_fizz, mask_buzz), axis=0)

    arr['str'][mask_fizz] = 'fizz'
    arr['str'][mask_buzz] = 'buzz'
    arr['str'][mask_fizzbuzz] = 'fizzbuzz'

    return arr.view(dtype=np.recarray)


if __name__ == '__main__':
    print('\n\nPlease enter the numbers to be evaluated by fizzbuzz:\n')
    minimum_n = input('minimum number:\t')
    maximum_n = input('maximum number:\t')

    # print('\n'.join(fizz_buzz(min_n=minimum_n, max_n=maximum_n)))

    result = fizz_buzz_np(min_n=minimum_n, max_n=maximum_n)
    for (idx, n) in enumerate(result):
        print('{:<3} {}'.format(result.int[idx], result.str[idx].decode()))
