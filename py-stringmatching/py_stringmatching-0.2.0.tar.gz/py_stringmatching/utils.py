import functools

import six

"""
This module defines a list of utility and validation functions.
"""


def sim_check_for_none(*args):
    if len(args) > 0 and args[0] is None:
        raise TypeError("First argument cannot be None")
    if len(args) > 1 and args[1] is None:
        raise TypeError("Second argument cannot be None")


def sim_check_for_empty(*args):
    if len(args[0]) == 0 or len(args[1]) == 0:
        return True


def sim_check_for_same_len(*args):
    if len(args[0]) != len(args[1]):
        raise ValueError("Undefined for sequences of unequal length")


def sim_check_for_string_inputs(*args):
    if not isinstance(args[0], six.string_types):
        raise TypeError('First argument is expected to be a string')
    if not isinstance(args[1], six.string_types):
        raise TypeError('Second argument is expected to be a string')


def sim_check_for_list_or_set_inputs(*args):
    if not isinstance(args[0], list):
        if not isinstance(args[0], set):
            raise TypeError('First argument is expected to be a python list or set')
    if not isinstance(args[1], list):
        if not isinstance(args[1], set):
            raise TypeError('Second argument is expected to be a python list or set')


def sim_check_tversky_parameters(alpha, beta):
        if alpha < 0 or beta < 0:
            raise ValueError('Tversky parameters should be greater than or equal to zero')


def sim_check_for_exact_match(*args):
    if args[0] == args[1]:
        return True


def sim_check_for_zero_len(*args):
    if len(args[0].strip()) == 0 or len(args[1].strip()) == 0:
        raise ValueError("Undefined for string of zero length")


def tok_check_for_string_input(*args):
    for i in range(len(args)):
        if not isinstance(args[i], six.string_types):
            raise TypeError('Input is expected to be a string')


def tok_check_for_none(*args):
    if args[0] is None:
        raise TypeError("First argument cannot be None")


def convert_bag_to_set(input_list):
    seen_tokens = {}
    output_set =[]
    for token in input_list:
        if seen_tokens.get(token) == None:
            output_set.append(token)
            seen_tokens[token] = True
    return output_set


def convert_to_unicode(input_string):
    """Convert input string to unicode."""
    if isinstance(input_string, bytes):
        return input_string.decode('utf-8')
    return input_string 
