import re


def get_only_base64_characters(arg):
    '''
        Returns only the base64 characters from the string, preserving order.

        Args:
            arg: The string that will have the non-base64 characters removed
        Returns:
            A string containing only base64 characters
    '''
    if not arg:
        return arg
    return re.sub('[^A-Za-z0-9+/=]', '', arg)


def contains_only_base64_characters(arg):
    '''
        Determines if arg contains only base64 character, regardless of order.
        Args:
            arg: the string being evaluated

        Returns:
            True: if the arg contains only base64 characters
            False: if is empty, None, or contains non-base64 characters
    '''
    if not arg:
        return False

    only_base64 = get_only_base64_characters(arg)
    return len(only_base64) is len(arg)


def is_base64(arg):
    '''
        Detremines if arg is of proper length and only contains valid base64 characters

        Args:
            arg: the string being considered
        Returns:
            True: if is a proper base64 string
            False: otherwise
    '''
    if not arg:
        return False

    pattern = re.compile('^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$')
    if pattern.match(arg):
        return True
    else:
        return False


def pad_string_until_proper_base64_length(arg):
    '''
        Pads arg until it is of proper length to be a valid base64 string.
        If arg begins with '=', will reverse it and move forward with padding.

        Raises ValueError if arg is not base64

        Args:
            arg: The string that will be padded

        Returns:
            padded base64 string, if base64
            None or empty string, if arg is None or empty
            otherwise, throws exception
    '''
    if not arg:
        return arg
    if not contains_only_base64_characters(arg):
        raise ValueError("This string has non-base64 characters: {}".format(arg))
    if arg[0] == '=':
        arg = arg[::-1]

    # Adding padding
    while(len(arg) % 4 != 0):
        arg += '='

    if not is_base64(arg):
        raise ValueError("This is not a valid Base64 string: {}".format(arg))

    return arg
