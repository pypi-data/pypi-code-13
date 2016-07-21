from .desktop import Desktop
from .shell import Shell
from .tui import Message, boolean_response


class Store:

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def __repr__(self):
        return '\n '.join('%s : %s' % (k, repr(v))
                          for (k, v) in self.__dict__.iteritems())


def main():
    # 1. Welcome the user.
    print("""
      _____        _
     |  __ \      | |
     | |  | | ___ | |  ___
     | |  | |/ _ \| __/ __|
     | |__| | (_) | |_\__ \\
     |_____/ \___/ \__|___/
    """)

    # 2. Basic input.
    #start = boolean_response(question='Would you like to start?', default=True)
    #print(start)

    # 3. Desktop backup and restore.
    d = Desktop()
    d.snapshot()
