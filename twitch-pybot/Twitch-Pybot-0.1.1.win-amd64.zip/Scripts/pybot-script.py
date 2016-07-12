#!C:\Python35\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Twitch-Pybot==0.1.1','console_scripts','pybot'
__requires__ = 'Twitch-Pybot==0.1.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('Twitch-Pybot==0.1.1', 'console_scripts', 'pybot')()
    )
