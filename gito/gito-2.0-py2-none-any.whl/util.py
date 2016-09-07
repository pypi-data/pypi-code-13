import os
import pathspec

BLOCK = 512

def istext(f_path):
    data = open(f_path).read(BLOCK)
    if "\0" in data:
        return False
    else:
        return True


def get_ignore_data(current_path):
    ignore_file = current_path + "/.gitignore"
    if os.path.exists(ignore_file):
        return open(ignore_file, "r").read()
    else:
        return None


def file_in_ignorelist(file_name, ignore_data):
    ignore_spec = pathspec.PathSpec.from_lines(pathspec.GitIgnorePattern,
                                               ignore_data.splitlines())
    if file_name in set(ignore_spec.match_files({file_name})):
        return True
    else:
        return False
