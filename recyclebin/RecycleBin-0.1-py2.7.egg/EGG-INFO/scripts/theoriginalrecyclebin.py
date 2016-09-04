from pyhooked import *

from subprocess import *
def recycle():
    check_output("start shell:RecycleBinFolder", shell=True).decode()

def handle_events(args):
    if isinstance(args, KeyboardEvent):
        if args.current_key == 'R' and args.event_type == 'key down' and 'Lmenu' in args.pressed_key:
            recycle()
hk = Hook()  # make a new instance of PyHooked
hk.handler = handle_events  # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
hk.hook() # hook into the events, and listen to the presses