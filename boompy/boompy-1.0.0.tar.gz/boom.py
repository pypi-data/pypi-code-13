from __future__ import print_function

import os
import sys
import argparse
import platform
import subprocess


__author__ = 'Bill Israel <bill.israel@gmail.com>'
__version__ =  '.'.join(map(str, (1, 0, 0)))

DEFAULT_DB = '~/.boomdb'


class Boom(dict):
    @classmethod
    def open(cls, filepath):
        obj = cls()
        obj.filepath = filepath

        if not os.path.exists(obj.filepath):
            open(obj.filepath, 'w').close()

        with open(obj.filepath, 'r') as f:
            for line in f.readlines():
                key, value = line.strip().split('\t', 1)
                obj[key] = value

        return obj

    def save(self):
        with open(self.filepath, 'w') as f:
            for key, value in self.iteritems():
                f.write('{}\t{}\n'.format(key, value))



class Clipboard(object):
    @staticmethod
    def copy(value):
        """Copy a string value to the system clipboard."""
        COPY_COMMAND = {
            'Darwin': ['pbcopy'],
            'Windows': ['clip'],
            'Linux': ['xclip', '-selection', 'clipboard']
        }
        cmd = COPY_COMMAND[platform.system()]
        pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        pipe.communicate(value)
        return not bool(pipe.returncode)


def main():
    parser = argparse.ArgumentParser(description='Simple command line snippets')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {} by {}'.format(__version__, __author__))
    parser.add_argument('key', type=str, nargs='?', help='The key to retrieve the value for')
    parser.add_argument('value', type=str, nargs='?', help='The value to set for the key')
    parser.add_argument('-d', '--database', dest='database', default=DEFAULT_DB,
                        help='File path where the boom database is located')
    parser.add_argument('--overwrite', action='store_true', default=False,
                        help='Overwrite any existing value for the given key')
    parser.add_argument('--delete', action='store_true', default=False,
                        help='Delete the given key')
    args = parser.parse_args()

    get_key = bool(args.key and not (args.value or args.delete))
    add_key = bool(args.key and args.value and not args.overwrite)
    delete_key = bool(args.key and not args.value and args.delete)
    update_key = bool(args.key and args.value and args.overwrite)

    try:
        snippets = Boom.open(os.path.expanduser(args.database))

        if get_key:
            if Clipboard.copy(snippets.get(args.key)):
                print("'{}' successfully copied to clipboard.".format(args.key))
        elif add_key:
            if snippets.has_key(args.key):
                raise ValueError('Key {} already exists'.format(args.key))

            snippets[args.key] = args.value
            print("'{}' is now '{}'.".format(args.key, args.value))
        elif delete_key:
            del snippets[args.key]
            print("'{}' has been removed.".format(args.key))
        elif update_key:
            snippets[args.key] = args.value
            print("'{}' is now '{}'.".format(args.key, args.value))
        else:
            if snippets:
                max_key_length = max(map(len, [key for key in snippets]))
                for key, value in snippets.iteritems():
                    print('{:<{}}\t{}'.format(key, max_key_length, value))

        snippets.save()
        return 0
    except Exception as ex:
        print('Error: {}'.format(ex), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

