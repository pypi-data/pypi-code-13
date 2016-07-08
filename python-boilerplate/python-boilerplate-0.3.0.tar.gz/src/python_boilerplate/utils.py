import os
import string
from contextlib import contextmanager

import unidecode


def pyname(name):
    """
    Converts a string of text into a valid python name.
    """

    name = unidecode.unidecode(name.strip().lower())
    valid = string.ascii_letters + string.digits + '_'
    char_list = []
    for i, char in enumerate(name):
        if char in valid:
            char_list.append(char)
        elif char in '- \t\n':
            char_list.append('_')

    # Join characters and take precautions against weird names
    name = ''.join(char_list)
    if not name:
        return 'project'
    elif name[0].isdigit():
        return 'py' + name
    else:
        return name


@contextmanager
def visit_dir(path):
    """Visit directory and come back after the with block is finish."""

    current_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(current_dir)


class AttrDict(dict):
    """
    Dictionary with attribute access to keys.
    """

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError

    def __setattr__(self, attr, value):
        self[attr] = value

    def sub(self, keys):
        if isinstance(keys, str):
            keys = keys.split()
        return AttrDict({k: self[k] for k in keys})