import json, os, subprocess, importlib, psutil, schedule
import autopy
import time
from time import sleep

import getpass
import gtk
import pygtk
import sys


class CaptureScreen:
    def __init__(self):
        # create a new window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(400, 100)
        window.set_title("Manual ScreenShot Comment DSS V.10")
        window.connect("delete_event", lambda w, e: window.destroy())

        vbox = gtk.VBox(False, 0)
        window.add(vbox)
        vbox.show()

        savepath = os.path.join(os.path.sep, 'plugins', 'collectors', 'manualscreenshot', 'raw',
                                str(int(time.time())) + '_' + getpass.getuser() + '_')
        full = os.getcwd() + savepath
        maxChar = 251 - len(full)
        print str(maxChar) + " is the max length"
        entry = gtk.Entry()
        entry.set_max_length(maxChar)
        entry.insert_text(" Enter Comment")
        entry.select_region(0, len(entry.get_text()))
        vbox.pack_start(entry, True, True, 0)
        entry.show()

        hbox = gtk.HBox(False, 0)
        vbox.add(hbox)
        hbox.show()

        button = gtk.Button(stock=gtk.STOCK_SAVE)
        button.connect("clicked", lambda w: SaveShot(window, entry))
        vbox.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        window.show()

def SaveShot(Window, entry):
    comment = entry.get_text()
    Window.window.destroy()
    sleep(.5)
    bitmap = autopy.bitmap.capture_screen()
    savepath = os.path.join(os.path.sep , 'plugins', 'collectors', 'manualscreenshot','raw', str(int(time.time()))+'_'+getpass.getuser()+'_'+comment)
    full = os.getcwd() + savepath
    bitmap.save(str(full) + '.png')
    print "screen shot taken"


