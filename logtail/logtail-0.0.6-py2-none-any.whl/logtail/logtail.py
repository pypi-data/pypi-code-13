from fnmatch import fnmatch
from time import sleep
import io
import os
import sys
import six
file_tracker = {}
stdout = io.open(1, "wb")


def set_title(title):
    term = os.environ.get("TERM")
    if term in ["xterm"]:
        print_binary(b"\x1B]0;%s\x07" % six.b(title))
    if term in ["screen"]:
        print_binary(b"\033k%s\033\\" % six.b(title))


def print_binary(data):
    stdout.write(data)
    stdout.flush()


def register_existing_files(search_path, name_match):
    for file_, size in get_changed(search_path, name_match, False):
        file_tracker[file_] = size


def get_changed(search_path, name_match, print_new=True):
    current = {}
    for path, dirs, files in os.walk(search_path):
        for f in files:
            if name_match is None or fnmatch(f, name_match):
                file_ = os.path.join(path, f)
                current[file_] = get_file_size(file_)

    for file_ in set(file_tracker) - set(current):
        print_binary(b"File removed: %s\n" % (six.b(file_)))
        file_tracker.pop(file_)

    for file_, size in current.items():
        if file_ not in file_tracker:
            if print_new:
                print_binary(b"New File: %s\n" % (six.b(file_)))
            file_tracker[file_] = 0

        if size != file_tracker[file_]:
            yield file_, size


def get_newest_file(search_path, name_match):
    current_time = 0
    current_file = None
    for path, dirs, files in os.walk(search_path):
        for f in files:
            if name_match is not None and not fnmatch(f, name_match):
                continue
            file_path = os.path.join(path, f)
            mtime = os.stat(file_path).st_mtime
            if mtime > current_time:
                current_time = mtime
                current_file = file_path
    return current_file


def get_file_size(path):
    return os.stat(path).st_size


def print_latest(current_file, size):
    set_title(current_file)
    if current_file in file_tracker:
        old_size = file_tracker[current_file]
        if size < old_size:
            print_binary(b"File Truncated: %s\n" % (six.b(current_file)))
            old_size = 0
            file_tracker[current_file] = 0
        if old_size != size:
            with open(current_file, "rb") as f:
                f.seek(old_size)
                print_binary(f.read(size - old_size))
            file_tracker[current_file] = size
    else:
        with open(current_file, "rb") as f:
            print_binary(f.read(size))
            file_tracker[current_file] = size


def check_args():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print_binary(b"Usage: taillogs <path> [<file glob>]\n")
        exit(1)

    if not os.path.exists(sys.argv[1]):
        e = IOError("No such file or directory: '{0}'".format(sys.argv[1]))
        e.errno = 2
        raise e

    if len(sys.argv) == 2:
        return sys.argv[1], "*.log"
    else:
        return sys.argv[1], sys.argv[2] or None


def main():
    path, match = check_args()
    register_existing_files(path, match)
    while True:
        for file_, size in get_changed(path, match):
            print_latest(file_, size)
        sleep(.1)


def editlatest():
    path, match = check_args()
    for editor in ["xdg-open", "subl", "vim", "vi", "nano", "pico"]:
        ret_code = os.system("{0} {1}".format(
            os.getenv('EDITOR', editor), get_newest_file(path, match)))
        if not ret_code:
            return ret_code

if __name__ == "__main__":
    main()
