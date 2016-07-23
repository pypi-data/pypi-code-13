"""The entry-point for the Dots application."""

from . import __version__
from .desktop import Desktop
from .tui import Message, boolean_response


def main():
    """Entry-point."""

    # Welcome the user.
    # pylint: disable=anomalous-backslash-in-string
    welcome = [
        "  _____        _", " |  __ \      | |", " | |  | | ___ | |  ___",
        " | |  | |/ _ \| __/ __|", " | |__| | (_) | |_\__ \\",
        " |_____/ \___/ \__|___/", "(Connect the dots!) v%s" % __version__, "",
        "(OS) =>   (Apps) =>   (Configuration) v",
        "(Perfection!) <= (Desktop) <= (Services)"
        "", "----------------------------------------", ""
    ]
    # pylint: enable=anomalous-backslash-in-string
    print('\n'.join(welcome))

    goodbye = Message('Goodbye!')

    snapshot_q = 'Would you like to take a snapshot of your current desktop?'
    take_snapshot = boolean_response(question=snapshot_q, default=True)
    if take_snapshot:
        Desktop().snapshot()
    else:
        goodbye.echo()
    Message('Your desktop has been saved in ~/.dots/desktops.json').echo()

    do_continue = ('Take a minute to modify the position and dimensions '
                   'values then hit enter to continue')
    boolean_response(do_continue, default=True)

    Desktop().restore()

    demo_q = 'Did you enjoy the demo of version %s?' % __version__
    demo_response = boolean_response(demo_q, default=True)

    if demo_response:
        m = ('Great! Feel free to post some suggestions to:\n'
             '    https://github.com/hoytnix/dots/issues')
        print(m)
    else:
        m = ('Sorry about that! Please file an issue at:\n'
             '    https://github.com/hoytnix/dots/issues')
        print(m)

    goodbye.echo()
