# -*- coding: utf-8 -*-
import os
import random
import re
import stat
import string

FILENAME_TEMPLATE = ".lzs__{}.txt"
DEFAULT_LEN = 80


def get_random_string():
    allowed_punctuation = re.sub(r'[\'"`\\/]', '', string.punctuation)
    chars = (string.ascii_letters + string.digits + allowed_punctuation)
    return ''.join(random.SystemRandom().choice(chars)
                   for _ in range(DEFAULT_LEN))


def is_name_valid(name):
    return True


def get_value(name, base_dir, length=DEFAULT_LEN,
              filename=None, permissions=None, generator=None):
    if generator is None:
        generator = get_random_string

    if filename is None:
        base_filename = FILENAME_TEMPLATE.format(name)
    else:
        base_filename = filename

    if not is_name_valid(name):
        raise ValueError('Invalid name')

    file_path = os.path.join(base_dir, base_filename)
    if os.path.isfile(file_path):
        with open(file_path) as fh:
            # Fix permissions if necessary
            return fh.read().strip()
    else:
        # generate new value
        new_value = generator()
        with open(file_path, 'w') as fh:
            fh.write(new_value + "\n")

        # Adjust file permissions: remove all 'others' permissions
        # See http://stackoverflow.com/a/25988623/1181370
        current_mode = stat.S_IMODE(os.lstat(file_path).st_mode)
        os.chmod(file_path, current_mode & ~stat.S_IRWXO)
        return new_value


class LazySecretValue(object):
    pass
