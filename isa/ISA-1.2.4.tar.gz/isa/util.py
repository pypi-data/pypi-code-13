import textwrap

import os
import tempfile


def create_file(content):
    """
    Create a file.

    :param content: the contents to put into the file
    :return: the file handle to the file
    """
    file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    file.write(textwrap.dedent(content))
    file.seek(0)
    return file


def remove_file(file):
    """
    Remove a file.

    :param file: the file handle to the INI file
    """
    if os.path.exists(file.name):
        return os.unlink(file.name)
    return False
