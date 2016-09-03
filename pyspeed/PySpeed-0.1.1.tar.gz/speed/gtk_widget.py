# This file is part of PySpeed - flexible progress bars for Python
# Written in August 2005
# Copyright (c) 2010 Rani Hod
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""
A GTK based graphical iteration context.
Part of the speed package.
"""

import sys, thread, time
from base import IterationContextBase
import xml.sax.saxutils as saxutils

#import pygtk
#pygtk.require("2.0")
import gtk, gtk.gdk

# --------------------------------------------------------------------------

ELAPSED_STYLE = '<tt>[Elapsed: <span foreground="#006000">%s</span>]</tt>'
LEFT_STYLE = '<tt>[Left: <span foreground="#800000">%s</span>]</tt>'
RATE_STYLE = '<tt>[<span foreground="#000080">%s</span> iters/sec]</tt>'
REPR_STYLE = '<tt>[Last element: <span foreground="#800080">%s</span>]</tt>'

# Set repr defaults
from repr import Repr
_repr = Repr()
_repr.maxlist = 10
_repr.maxother = 30

class Frame(gtk.Frame):
    def __init__(self):
        gtk.Frame.__init__(self)
        self.set_shadow_type(gtk.SHADOW_NONE)

        self._table = gtk.Table(3, 3, True)
        self._progress = gtk.ProgressBar()
        self._elapsed = gtk.Label()
        self._left = gtk.Label()
        self._rate = gtk.Label()
        self._repr = gtk.Label()

        self._table.attach(
            self._progress, 0, 3, 0, 1, gtk.EXPAND|gtk.FILL, gtk.FILL)
        self._table.attach(
            self._elapsed, 0, 1, 1, 2, gtk.EXPAND|gtk.FILL, gtk.FILL)
        self._table.attach(
            self._left, 1, 2, 1, 2, gtk.EXPAND|gtk.FILL, gtk.FILL)
        self._table.attach(
            self._rate, 2, 3, 1, 2, gtk.EXPAND|gtk.FILL, gtk.FILL)
        self._table.attach(
            self._repr, 0, 3, 2, 3, gtk.EXPAND|gtk.FILL, gtk.FILL)

        self.add(self._table)

        self._progress.show()
        self._elapsed.show()
        self._left.show()
        self._rate.show()
        self._repr.show()
        self._table.show()
    
    def reset(self, length, is_repr):
        if length is None:
            progress_str = "0/?"
        else:
            progress_str = "0/%d (0%%)" % length
        
        if is_repr:
            repr_str = REPR_STYLE % "?"
        else:
            repr_str = ""
        
        self._progress.set_fraction(0.)
        self._progress.set_text(progress_str)
        self._elapsed.set_markup(ELAPSED_STYLE % "00:00:00")
        self._left.set_markup(LEFT_STYLE % "??:??:??")
        self._rate.set_markup(RATE_STYLE % "?")
        self._repr.set_markup(repr_str)
        
    def _format_time(secs):
        gm = time.gmtime(secs)
        if secs < 60*60:
            return time.strftime("%M:%S", gm)
        else:
            res = time.strftime("%H:%M:%S", gm)
            days = secs // (60*60*24)
            if days:
                res = "%dd " % days + res
            return res
    _format_time = staticmethod(_format_time)

    def set(self, elem_repr, idx, length, elapsed_time):
        if not idx: return

        elapsed_str = self._format_time(elapsed_time)
        rate_str = "%5.2f" % (idx / elapsed_time)

        if length is None:
            self._progress.pulse()
            progress_str = "%d/?" % idx
        else:
            fraction = float(idx) / length
            self._progress.set_fraction(fraction)
            progress_str = "%d/%d (%d%%)" % (idx, length, int(100*fraction))
            projected_time = elapsed_time / fraction
            left_time = projected_time - elapsed_time
            left_str = self._format_time(left_time)
            self._left.set_markup(LEFT_STYLE % left_str)

        self._elapsed.set_markup(ELAPSED_STYLE % elapsed_str)
        self._rate.set_markup(RATE_STYLE % rate_str)
        self._progress.set_text(progress_str)
        if elem_repr is not None:
            # Escape special characters because it's a markup label
            self._repr.set_markup(REPR_STYLE % saxutils.escape(elem_repr))

# --------------------------------------------------------------------------

class GTKProgress(object):
    title_name = 'PySpeed'
    
    def __init__(self,title=None):
        if title is not None:
            self.title_name = title
        self._create_widgets()
        self._frames = []

    def _create_widgets(self):
        self._window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self._vbox = gtk.VBox(False, 3)
        self._dismiss = gtk.Button("_Dismiss")

        self._window.set_title(self.title_name)
        self._window.connect('delete_event', self.__cb_delete_event)
        self._window.add(self._vbox)

        self._vbox.pack_end(self._dismiss, False, True)
        self._vbox.show()

        self._dismiss.connect_object(
            'clicked', self.__cb_delete_event, self._window, None)
        self._dismiss.set_flags(gtk.CAN_DEFAULT)
        self._dismiss.grab_default()
        self._dismiss.show()
    
    def __cb_delete_event(self, window, event):
        self.hide_window(False)
        return True

    def reset(self):
        self.hide_window()

    def allocate_frame(self, level, length):
        if len(self._frames) <= level:
            gtk.gdk.threads_enter()
            frame = Frame()
            self._frames.append(frame)
            self._vbox.pack_start(frame, False, True)
            gtk.gdk.threads_leave()
        else:
            frame = self._frames[level]

        #init frame
        gtk.gdk.threads_enter()
        frame.reset(length, True)
        frame.show()
        gtk.gdk.threads_leave()

        return frame

    def update_title(self, acquire_thread_lock=True):
        if acquire_thread_lock:
            gtk.gdk.threads_enter()

        self._window.set_title('%s<%s>' %
                               (self.title_name,
                                ":".join([f._progress.get_text()
                                          for f in self._frames]) )
                               )
        
        if acquire_thread_lock:
            gtk.gdk.threads_leave()

    def show_window(self):
        gtk.gdk.threads_enter()
        self._window.resize(1, 1)
        self._window.set_position(gtk.WIN_POS_CENTER)
        self._window.show()
        gtk.gdk.threads_leave()

    def hide_window(self, acquire_thread_lock=True):
        if acquire_thread_lock:
            gtk.gdk.threads_enter()

        for frame in self._frames:
            frame.hide()
        self._window.hide()
        self._window.set_title(self.title_name)

        if acquire_thread_lock:
            gtk.gdk.threads_leave()

# --------------------------------------------------------------------------

class GTKIterationContext(IterationContextBase):
    NAME = "graph"

    def __init__(self, it, level, repr=None):
        IterationContextBase.__init__(self, it, level)
        self._frame = theWidget.allocate_frame(self._level, self._it._len)
        self._should_show_window = (self._level == 0)
        self._repr = repr or _repr.repr

    def update(self, elem):
        est = self._it.estimate_remaining()
        fraction, iter_rate, elapsed_time, remaining_time = est

        n = self._it._last_update[0]

        gtk.gdk.threads_enter()
        self._frame.set(self._repr(elem), n, self._it._len, elapsed_time)
        theWidget.update_title(False)
        gtk.gdk.threads_leave()

        if self._should_show_window:
            self._should_show_window = False
            theWidget.show_window()

    def cleanup(self):
        if self._level == 0:
            theWidget.hide_window()
        #!gtk.gdk.threads_enter()
        #!self._frame.hide()
        #!gtk.gdk.threads_leave()

# --------------------------------------------------------------------------

# init gtk
if not gtk.main_level():
    gtk.set_interactive(False)
    if '_GTK_THREADS_INIT' not in globals():
        gtk.gdk.threads_init()
        _GTK_THREADS_INIT = True
    thread.start_new_thread(gtk.main, ())

theWidget = GTKProgress()
