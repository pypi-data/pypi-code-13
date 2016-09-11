#!/usr/bin/env python

import os
import requests
import argparse
from os.path import expanduser
import signal

if os.environ.get('TRAVIS') != 'true':
    import pygtk

    pygtk.require('2.0')
    import gtk

    try:
        import appindicator
    except ImportError:
        import appindicator_replacement as appindicator

    from appindicator_replacement import get_icon_filename


class HblockApp:
    HOSTS_URL = "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
    UPDATE_URL = "https://github.com/artiya4u/hblock#upgrade"
    ABOUT_URL = "https://github.com/artiya4u/hblock"

    def __init__(self, args):
        # create an indicator applet
        self.ind = appindicator.Indicator("HBlock", "HBlock", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_icon(get_icon_filename("hblock.png"))
        
        # Load the database
        home = expanduser("~")
        host_path = home + '/.hblock.hosts'
        self.block_state = False
        if not os.path.isfile(host_path):
            requests.get(self.HOSTS_URL)
            with open(host_path, 'wb') as handle:
                response = requests.get(self.HOSTS_URL, stream=True)

                if not response.ok:
                    # Something went wrong
                    pass

                for block in response.iter_content(1024):
                    handle.write(block)
                self.block_state = True
        else:
            self.block_ads()

        # create a menu
        self.menu = gtk.Menu()

        btn_comments = gtk.CheckMenuItem("Block Ads")
        btn_comments.show()
        btn_comments.set_active(self.block_state)
        btn_comments.connect("activate", self.toggle_adblock)
        self.menu.append(btn_comments)

        self.menu.show()

        self.ind.set_menu(self.menu)

    def toggle_adblock(self, widget):
        if self.block_state:
            self.unblock_ads()
        else:
            self.block_ads()

    def block_ads(self):
        if not os.path.isfile('~/.hosts.old'):
            os.system("cp /etc/hosts ~/.hosts.old")
            ret_value = os.system("""gksu cp ~/.hblock.hosts /etc/hosts \
            --message 'HBlock requires administrator right to start blocking ads.'""")
            if ret_value == 0:
                self.ind.set_icon(get_icon_filename("hblock-enabled.png"))
                self.block_state = not self.block_state

    def unblock_ads(self):
        ret_value = os.system("""gksu 'cp /etc/hosts.hblock /etc/hosts' \
            --message 'HBlock requires administrator right to stop blocking ads.'""")
        if ret_value == 0:
            os.system("""rm ~/.hosts.old""")
            self.ind.set_icon(get_icon_filename("hblock-disabled.png"))
            self.block_state = not self.block_state

    # ToDo: Handle keyboard interrupt properly
    def quit(self, widget, data=None):
        self.unblock_ads()
        gtk.main_quit()

    def run(self):
        signal.signal(signal.SIGINT, self.quit)
        gtk.main()
        return 0


def main():
    parser = argparse.ArgumentParser(description='Hostname Adblocker in your System Tray')
    args = parser.parse_args()
    indicator = HblockApp(args)
    indicator.run()


if __name__ == '__main__':
    main()
