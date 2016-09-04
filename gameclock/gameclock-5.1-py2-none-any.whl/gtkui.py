# -*- coding: utf-8 -*-
# The GTK graphical user interface

import pygtk
pygtk.require('2.0')
import pango
import gtk
from glib import GError
import gobject
import time
import os
import pkg_resources

from gameclock.game import *
import gameclock.clock
import gameclock.sound
from gameclock import __version__, __license__, __copyright__

import gameclock.i18n


class GameclockUI:
    """this class handles most of the UI and turned-based logic
    
    It is not designed for UI-abstraction yet, but could be, if the
    turn-based logic is ripped in a seperate class
    """

    first_clock = None
    cur_clock = None
    clock_widget_cnt = 0
    # the game this UI references
    game = None
    # in ms, clocks are incremented every time this timeout ends
    sec_loop_timeout = 500
    # in ms, the same as above, in milisecond mode
    ms_loop_timeout = 100
    # used in the fullscreen toggle
    menubar = None

    ui_desc = """
<ui>
  <menubar name="menubar">
    <menu action="game">
      <menu action="new">
        <!-- filled in dynamically below -->
      </menu>
      <menuitem action="pause" />
      <menuitem action="restart" />
      <menuitem name="Full screen" action="fullscreen" />
      <menuitem name="Quit" action="quit" />
    </menu>
    <menu action="settings">
      <menuitem action="time" />
      <menuitem action="players" />
      <menuitem action="sound" />
      <menu action="theme">
        <!-- filled in dynamically below -->
      </menu>
    </menu>
    <menu action="help">
      <menuitem name="About" action="about" />
      <menuitem name="Keyboard shortcuts" action="keyboard" />
    </menu>
  </menubar>
</ui>
"""

    themes = [('default', _('Default'), _('Use the default theme'), None),
              ('green', _('Green'), _('Selected player is green, dead player is red, normal background black (4.0 default)'), """
style "clockui" {
  bg[NORMAL] = "black"
  fg[NORMAL] = "white"
  bg[SELECTED] = "red"
  fg[SELECTED] = "black"
  bg[ACTIVE] = "green"
  fg[ACTIVE] = "black"
}

widget "*.clockui.GtkEventBox" style "clockui"
widget "*.clockui.*Label" style "clockui"
"""
              ),
              ('blue', _('Blue'), _('Selected player is blue, dead player is red, normal background black'), """
style "clockui" {
  bg[NORMAL] = "black"
  fg[NORMAL] = "white"
  bg[SELECTED] = "red"
  fg[SELECTED] = "black"
  bg[ACTIVE] = "blue"
  fg[ACTIVE] = "white"
}

widget "*.clockui.GtkEventBox" style "clockui"
widget "*.clockui.*Label" style "clockui"
"""),
          ]

    def __init__(self, verbose=0, fullscreen=False, **settings):
        """the UI constructor

we take settings in to allow unit tests to override the default game
"""
        self.verbose = verbose
        self.fullscreen = fullscreen
        self.debug('running with verbosity: %d' % self.verbose)

        # the default game
        self.game = LightningChessGame(**settings)

        self.ui_actions = [('game', None, _('_Game')),
                           ('new', gtk.STOCK_NEW, _('_New')),
                           ('pause', gtk.STOCK_MEDIA_PLAY, _('Start'), '<control>p',
                            _('Start/pause game'), self.handle_pause),
                           ('restart', gtk.STOCK_REFRESH, _('Restart'), '<control>r',
                            _('Restart game'), self.handle_restart),
                           ('fullscreen', gtk.STOCK_FULLSCREEN, _('_Full screen'), '<control>f',
                            _('Full screen mode'), self.handle_fullscreen),
                           ('quit', gtk.STOCK_QUIT, _('_Quit'), '<control>q',
                            _('Quit the Program'), gtk.main_quit),
                           ('settings', None, _('_Settings')),
                           ('time', None, _('_Set time...'), None,
                            _('Set the starting time of clocks'), self.handle_time),
                           ('players', None, _('_Players...'), None,
                            _('Set the number of players and starting player'), self.handle_players),
                           ('theme', None, _('Theme')),
                           ('help', None, _('_Help')),
                           ('about', None, _('_About'), None,
                            _('More information about this software'), self.about_dialog),
                           ('keyboard', None, _('Keyboard shortcuts'), None,
                            _('Display the available keyboard shortcuts'), self.shortcuts_dialog),
                           ]
        # setup icon
        try:
            icon = pkg_resources.resource_filename(pkg_resources.Requirement.parse("gameclock"), 'gameclock.svg')
            gtk.window_set_default_icon_from_file(icon)
        except GError as e:
            # misconfigured, ignore
            self.debug("could not find icon: %s" % e)
        except pkg_resources.DistributionNotFound:
            # not installed system-wide, ignore
            pass
        finally:
            # last resort, try the FHS and source directories
            for icon in ["/usr/share/icons/hicolor/scalable/apps/gameclock.svg",
                         "/usr/share/pixmaps/gameclock.xpm",
                         os.path.dirname(__file__) + "/../gameclock.svg"]:
                if os.path.exists(icon):
                    gtk.window_set_default_icon_from_file(icon)

        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # handle window close events
        self.window.connect("delete_event", lambda a, b: False)
        self.window.connect("destroy", gtk.main_quit)
    
        self.window.connect('key_press_event', self.handle_key_press)

        event_box = gtk.EventBox()
        self.window.add(event_box)
        event_box.show()
        # catch clicks as end turn
        event_box.set_extension_events(gtk.gdk.EXTENSION_EVENTS_ALL)
        event_box.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        event_box.connect("button_press_event", self.handle_move)

        # main window consists of a vbox containing two hbox
        self.vlayout = vlayout = gtk.VBox(False, 0)
        event_box.add(vlayout)

        # Create a UIManager instance
        uimanager = gtk.UIManager()

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.window.add_accel_group(accelgroup)

        # Create an ActionGroup
        actiongroup = gtk.ActionGroup('UIManagerExample')
        self.actiongroup = actiongroup

        # Create actions
        actiongroup.add_actions(self.ui_actions)
        actiongroup.get_action('quit').set_property('short-label', _('_Quit'))
        self.soundaction = gtk.ToggleAction('sound',
                                            _('_Sound'),
                                            _('Enable/disable sound'),
                                            None)
        actiongroup.add_action(self.soundaction)

        # Add a UI description
        uimanager.add_ui_from_string(self.ui_desc)

        # add the games from the game module to the UI
        i = 0
        radiogroup = None
        for name, cls in enumerate_games():
            name = _(cls.nice_name())
            self.debug('adding game %s %s' % (name, cls))
            # add the given entry as an action to the menu
            uimanager.add_ui(uimanager.new_merge_id(),
                             '/menubar/game/new', name, cls.__name__,
                             gtk.UI_MANAGER_AUTO, True)
            action = gtk.RadioAction(cls.__name__, name,
                                     _(cls.__doc__), None, i)
            if cls == self.game.__class__:
                action.set_current_value(i)
            i += 1
            action.connect('activate', self.handle_type, cls)
            if radiogroup is None:
                radiogroup = action
            else:
                action.set_group(radiogroup)
            actiongroup.add_action(action)

        # setup theme menu
        i = 0
        radiogroup = None
        for name, label, tooltip, rcstring in self.themes:
            uimanager.add_ui(uimanager.new_merge_id(),
                             '/menubar/settings/theme',
                             name, name, gtk.UI_MANAGER_AUTO, True)
            action = gtk.RadioAction(name, label, tooltip, None, i)
            i += 1
            action.connect('activate', self.handle_theme, name)
            if radiogroup is None:
                radiogroup = action
            else:
                action.set_group(radiogroup)
            actiongroup.add_action(action)
        action.set_current_value(0)

        # Add the actiongroup to the uimanager
        uimanager.insert_action_group(actiongroup, 0)

        # this is to make the tooltip appear, rather silly...
        # see https://www.daa.com.au/pipermail/pygtk/2010-September/018978.html
        uimanager.connect('connect-proxy', self.uimanager_connect_proxy)

        # Create a MenuBar
        self.menubar = uimanager.get_widget('/menubar')
        uimanager.get_widget('/menubar/help').set_right_justified(True)
        self.uimanager = uimanager

        self.vlayout.pack_start(self.menubar, False, True, 0)
        self.menubar.show()

        # the clocks
        self.clock_table = gtk.Table(1, 2, True)
        self.clock_table.show()
        vlayout.pack_start(self.clock_table, True, True, 0)

        vlayout.show()

        # we need to flip this because handle_fullscreen
        # *toggles* the fullscreen
        self.fullscreen = not fullscreen
        self.handle_fullscreen()

        # sound support, depends on python-pygame and sound-theme-freedesktop
        try:
            self.sounds = gameclock.sound.Player({'dead': '/usr/share/sounds/freedesktop/stereo/complete.oga',
                                                  'move': '/usr/share/sounds/freedesktop/stereo/dialog-information.oga'},
                                                 self.soundaction.get_active)
        except (gameclock.sound.AudioDriverException, IOError, ImportError) as e:
            self.debug('sound disabled: %s' % e)
            self.sounds = gameclock.sound.DumbPlayer()

    def uimanager_connect_proxy(self, uimgr, action, widget):
        tooltip = action.get_property('tooltip')
        if isinstance(widget, gtk.MenuItem) and tooltip:
            widget.set_tooltip_text(tooltip)

    def main(self):
        """create the main user interface with GTK"""

        if self.game:
            self.setup_clocks()
            self.window.show()
            gtk.main()

    def setup_clocks(self):
        for c in self.clock_table.get_children():
            self.clock_table.remove(c)
            del c
        q = self.game.first_clock
        self.first_clock = None
        x = 1
        y = -1
        prev = None
        for i in range(self.game.players):
            clock = ClockUI(self, q)
            q = q.next
            if prev is not None:
                prev.next = clock
            prev = clock
            if self.first_clock is None:
                self.cur_clock = self.first_clock = clock
            if x == 1:
                x = 0
                y = y + 1  # new row
            else:
                x = 1
            self.clock_table.attach(clock, x, x+1, y, y+1)
        cols = 2
        rows = (self.game.players - 1) / cols + 1
        self.clock_table.resize(rows, cols)
        self.refresh()
        self.debug("now at %d clocks, table size is %dX%d"
                   % (self.game.players, rows, cols))

    def next(self):
        """change the current clock

        simply switch the clock in the game engine and rehilight
        """
        self.game.next()
        self.cur_clock = self.cur_clock.next
        if not self.cur_clock:
            self.cur_clock = self.first_clock

    def status(self, text):
        self.debug(text)
        # self.turns.set_label(text)

    def debug(self, text):
        if self.verbose:
            t = ""
            state = ""
            if self.verbose > 1:
                t = "[%f] " % time.time()
                if self.verbose > 2:
                    state = "\n  game engine state: %s" % self.game
            print t + text + state

    def refresh(self):
        p = self.first_clock
        while p:
            p.refresh()
            p = p.next
        self.hilight()
        
    def refresh_current(self):
        """refresh the active clock
        
        this handler is ran periodically through a timeout signal to
        make sure that the current clock is updated

        """

        keep_handler = self.game.running()

        # in hourglass, we just update both clocks all the time
        if isinstance(self.game.first_clock, gameclock.clock.HourglassClock):
            # check if any clock is below 60s
            p = self.first_clock
            while p:
                p = p.next
                # if we are in a sprint, it will switch the timeout handler
                # ditch ours
                if keep_handler and p:
                    keep_handler = not p.check_sprint()
            # refresh both clocks
            self.refresh()
            return keep_handler

        # if we are in a sprint, it will switch the timeout handler, ditch ours
        if keep_handler:
            keep_handler = not self.cur_clock.check_sprint()

        self.cur_clock.refresh()
        return keep_handler

    def hilight(self):
        """hilight the proper clocks with proper colors
        
        this is 'transparent' for the inactive clock and colored for the
        active clock. the color depends on wether the clock is 'dead' or
        not
        """
        p = self.first_clock
        while p:
            p.hilight(p == self.cur_clock)
            p = p.next

    def handle_key_press(self, widgets, event):
        keyname = gtk.gdk.keyval_name(event.keyval)

        # see this FAQ for more information about keycodes:
        # http://faq.pygtk.org/index.py?file=faq05.005.htp&req=edit
        # notice how we do not handle the arrow, home and num pad keys
        if event.state & gtk.gdk.CONTROL_MASK or \
           event.state & gtk.gdk.MOD1_MASK:
            # gtk.gdk.SHIFT_MASK is okay
            self.debug("key pressed with mod/control ignored")
        elif (keyname == 'Shift_L' or keyname == 'Caps_Lock'
              or keyname == 'Alt_L' or keyname == 'Super_L'
              or event.hardware_keycode == 49  # ~
              or event.hardware_keycode in range(52, 56)  # z-b
              or event.hardware_keycode in range(38, 42)  # a-g
              or event.hardware_keycode in range(23, 28)  # tab-q-t
              or event.hardware_keycode in range(10, 15)  # 1-6
              or event.hardware_keycode in range(67, 70)):  # F1-F4
            if self.game.cur_clock == self.game.first_clock:
                self.handle_move()
        elif (keyname == 'Shift_R' or keyname == 'Return'
              or keyname == 'Alt_R' or keyname == 'Super_R'
              or event.hardware_keycode in range(57, 61)  # n-/
              or event.hardware_keycode in range(43, 48)  # h-'
              or event.hardware_keycode in range(29, 35)  # y-]
              or event.hardware_keycode in range(16, 22)  # 7-backspace
              or event.hardware_keycode in range(75, 76)  # F9-F10
              or event.hardware_keycode in range(95, 96)  # F10-F11 (wtf?)
              or keyname == 'Menu' or event.hardware_keycode == 51):  # \
            if self.game.cur_clock != self.game.first_clock:
                self.handle_move()
        elif event.hardware_keycode in range(71, 74):  # F5-F8 is pause
            self.handle_pause()
        elif keyname == 'space':
            self.handle_move()
        elif keyname == 'Escape':
            if self.fullscreen:
                self.handle_fullscreen()
        self.debug("key %s (%d/%d) was pressed" %
                   (keyname, event.keyval, event.hardware_keycode))

    def handle_fullscreen(self, action=None):
        if self.fullscreen:
            self.window.unfullscreen()
            self.menubar.show()
        else:
            self.window.fullscreen()
            self.menubar.hide()
        self.fullscreen = not self.fullscreen

    def handle_type(self, action, game):
        self.debug("setting up for game %s" % game)
        if action.get_active():
            self.game = game()
            # XXX: this looses all time settings
            self.setup_clocks()
            self.uimanager.get_action('/menubar/settings').set_sensitive(True)

    def handle_restart(self, action=None):
        """restart the game with the backed up settings"""
        self.game.pause()
        self.game = self.game_restart.copy()
        self.setup_clocks()
        self.uimanager.get_action('/menubar/settings').set_sensitive(True)

    def handle_time(self, action):
        """handle the time selection menu

this generates a popup window to allow the user to change the times,
including fischer-like delays, and that will then call
handle_time_response() to process the results.
"""
        window = gtk.Dialog(_("Change time settings"),
                            self.window,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        window.set_default_response(gtk.RESPONSE_ACCEPT)
        window.connect("delete_event", lambda a, b: False)
        window.connect("destroy", lambda a: window.destroy)
        window.connect('response', self.handle_time_response)

        # the widgets to change the starting time
        minutes, milliseconds = divmod(self.game.time, 60000)
        seconds = float(milliseconds) / 1000
        self.minutes_val = gtk.Adjustment(minutes, 0, 1440, 1, 10, 0)
        self.seconds_val = gtk.Adjustment(seconds, 0, 59, 1, 10, 0)
        minutes_val_btn = gtk.SpinButton(self.minutes_val, 1.0, 0)
        seconds_val_btn = gtk.SpinButton(self.seconds_val, 1.0, 0)
        minutes_val_btn.show()
        seconds_val_btn.show()
        clock_controls = gtk.HBox(False, 0)
        label = gtk.Label(_("Time limit: "))
        label.show()
        clock_controls.pack_start(label, False, False)
        clock_controls.pack_start(minutes_val_btn, False, False)
        clock_controls.pack_start(seconds_val_btn, False, False)
        clock_controls.show()
        window.vbox.pack_start(clock_controls, False, False, 10)

        if isinstance(self.game, gameclock.game.AbstractDelayGame):
            controls = gtk.HBox(False, 0)
            label = gtk.Label(_('Delay: '))
            label.show()
            controls.pack_start(label, True, False, 0)
            self.delay_val = gtk.Adjustment(self.game.delay/1000,
                                            1, 10000, 1, 10, 0)
            self.delay_val_btn = gtk.SpinButton(self.delay_val, 0.0, 0)
            self.delay_val_btn.show()
            controls.pack_start(self.delay_val_btn, False, False, 0)
            controls.show()
            window.vbox.pack_start(controls, False, False, 0)

        if isinstance(self.game, gameclock.game.AbstractGoGame):
            controls = gtk.HBox(False, 0)
            label = gtk.Label(_('Number of Byo-yomi: '))
            label.show()
            controls.pack_start(label, True, False, 0)
            self.byoyomi_val = gtk.Adjustment(self.game.byoyomi,
                                              1, 100, 1, 10, 0)
            self.byoyomi_val_btn = gtk.SpinButton(self.byoyomi_val, 0.0, 0)
            self.byoyomi_val_btn.show()
            controls.pack_start(self.byoyomi_val_btn, False, False, 0)
            controls.show()
            window.vbox.pack_start(controls, False, False, 0)

        window.show()

    def handle_time_response(self, dialog, response_id):
        """handle the time selected in the handle_time() dialog"""
        dialog.destroy()
        if response_id == gtk.RESPONSE_ACCEPT:
            minutes = self.minutes_val.get_value()
            seconds = self.seconds_val.get_value()
            time = ((minutes * 60) + seconds) * 1000
            self.game.set_time(time)
            if isinstance(self.game, gameclock.game.AbstractDelayGame):
                self.game.set_delay(int(self.delay_val.get_value() * 1000))
            if isinstance(self.game, gameclock.game.AbstractGoGame):
                self.game.set_byoyomi(int(self.byoyomi_val.get_value()))
            self.refresh()

    def handle_players(self, action):
        window = gtk.Dialog(_("Change players settings"),
                            self.window,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        window.set_default_response(gtk.RESPONSE_ACCEPT)
        window.connect("delete_event", lambda a, b: False)
        window.connect("destroy", lambda a: window.destroy)
        window.connect('response', self.handle_players_response)

        hbox = gtk.HBox(False, 0)
        label = gtk.Label(_('Number of players: '))
        label.show()
        self.players_val = gtk.Adjustment(self.game.players,
                                          1, 10000, 1, 10, 0)
        players_val_btn = gtk.SpinButton(self.players_val, 0.0, 0)
        players_val_btn.show()
        hbox.pack_start(label, False, False, 10)
        hbox.pack_start(players_val_btn, False, False, 0)
        hbox.show()
        window.vbox.pack_start(hbox, False, False, 0)

        # the main toggle button, used by various signal handlers
        hbox = gtk.HBox(False, 0)
        label = gtk.Label(_('Starting player: '))
        label.show()
        self.left_starts = gtk.RadioButton(None, _('Left'))
        self.left_starts.set_active(True)
        self.left_starts.show()
        button = gtk.RadioButton(self.left_starts, _('Right'))
        button.show()
        hbox.pack_start(label, False, False, 10)
        hbox.pack_start(self.left_starts, False, False, 10)
        hbox.pack_start(button, False, False, 10)
        hbox.show()
        window.vbox.pack_start(hbox, False, False, 0)

        window.show()

    def handle_players_response(self, dialog, response_id):
        """handle the time selected in the handle_time() dialog"""
        dialog.destroy()
        if response_id == gtk.RESPONSE_ACCEPT:
            self.game.resize(int(self.players_val.get_value()))
            self.setup_clocks()
            if not self.left_starts.get_active():
                self.next()
                self.hilight()

    def handle_theme(self, action, theme):
        for name, label, tooltip, rcstring in self.themes:
            if name == theme:
                if rcstring is None:
                    # special: reset all styles
                    if hasattr(self, 'default_style'):
                        p = self.first_clock
                        while p:
                            p.evbox.set_style(self.default_style)
                            p.label.set_style(self.default_style)
                            p = p.next
                else:
                    if not hasattr(self, 'default_style'):
                        # store the previous style so we can restore it
                        self.default_style = self.first_clock.label.get_style()
                    gtk.rc_parse_string(rcstring)
                    # necessary for changes to apply
                    gtk.rc_reset_styles(self.window.get_settings())

    def handle_move(self, widget=None, event=None):
        """handle end turn events
        
        this passes the message to the gaming engine as quickly as
        possible then goes around updating the UI
        """
        # it may be that we need to start the display
        if not self.game.running():
            self.start_game()
        elif not self.first_clock.next:
            self.game.pause()
        else:
            self.move()

        # some reason it doesn't work to just update the old clock label
        # we need to update both
        self.refresh()
        self.hilight()
        self.debug("turn finished")
        self.sounds.play('move')

    def handle_pause(self, action=None):
        """pause handler
        
        just a stub for the game engine for now
        """
        moveaction = self.uimanager.get_action('/menubar/game/pause')
        if not self.game.running() and moveaction.get_label() == 'Start':
            # XXX: hack. we should be able to differentiate a paused
            # game (started and not running) from a game about to
            # started (not running but not started)
            self.start_game()
        elif self.game.pause():
            moveaction.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            moveaction.set_label(_('Resume'))
            self.status(_('game paused'))
        else:
            moveaction.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
            moveaction.set_label(_('Pause'))
            self.status(_('game resumed'))
            # the timeout handler is removed when we pause, resume
            self.timeout_source = gobject.timeout_add(self.loop_timeout,
                                                      self.refresh_current)

    def start_game(self):
        # backup the game settings for a possible restart
        self.game_restart = self.game.copy()
        self.next()
        self.hilight()
        self.game.start()
        self.loop_timeout = self.sec_loop_timeout
        self.timeout_source = gobject.timeout_add(self.loop_timeout,
                                                  self.refresh_current)

        moveaction = self.uimanager.get_action('/menubar/game/pause')
        moveaction.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
        moveaction.set_label(_('Pause'))

        self.status(_("game running"))
        self.debug("refresh rate %dms" % self.loop_timeout)
        self.uimanager.get_action('/menubar/settings').set_sensitive(False)

    def move(self):
        self.game.move()
        # update the current clock pointer
        self.cur_clock = self.cur_clock.next
        if not self.cur_clock:
            self.cur_clock = self.first_clock

    def players(self):
        """return the number of players configured"""
        try:
            return int(self.players_val.get_value())
        except:
            return ChessGame.players

    def shortcuts_dialog(self, action=None):
        window = gtk.MessageDialog(self.window,
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK)
        # window.set_default_response(gtk.RESPONSE_OK)
        # little help
        window.set_markup(_("""<big>Keyboard shortcuts</big>

<b>shift</b> and <b>space</b> keys end turns
<b>control-q</b> quits
<b>control-n</b> starts a new game
<b>control-f</b> enables fullscreen mode
<b>control-p, F5-F8</b> pause the game"""))
        window.format_secondary_text(_("""Left side of the keyboard ends left side's turn and vice-versa for right turn.

We do not currently handle the numpad and arrow keys as we can't tell if they are present or not (e.g. laptops) and that would favor too much right right side if it is present."""))
        window.connect("response", lambda a, b: window.destroy())
        window.show()

    def about_dialog(self, action=None):
        dialog = gtk.AboutDialog()
        dialog.set_version(__version__)
        dialog.set_copyright(__copyright__)
        dialog.set_license(__license__)
        dialog.set_comments(_("A simple game clock to be used for Chess or any board game."))
        dialog.set_website("https://0xacab.org/anarcat/gameclock/")
        dialog.connect("response", lambda a, b: dialog.destroy())
        dialog.show()


class ClockUI(gtk.VBox):
    """this class is used to encapsulate the various controls related with a clock"""

    # like the game Clock, it is a linked list
    next = None
    ui = None

    def __init__(self, ui, clock, next=None):
        gtk.VBox.__init__(self)
        # for theming
        self.set_name('clockui')
        self.ui = ui
        self.next = next
        self.clock = clock
        self.dead_sound_played = False

        self.moves = gtk.Label()
        self.moves.show()
        # for theming to apply
        e = gtk.EventBox()
        e.add(self.moves)
        e.show()
        self.pack_start(e, False)

        self.label = gtk.Label()
        self.label.modify_font(pango.FontDescription("72"))
        self.label.show()
        self.guess_format()

        # event boxes to be able to color the labels
        self.evbox = gtk.EventBox()
        self.evbox.add(self.label)
        self.evbox.show()
        self.pack_start(self.evbox, True, True)

        self.show()

    def refresh(self):
        self.ui.debug("clock time: %f" % self.clock.get_time())
        self.guess_format()
        self.moves.set_label(self.clock.moves_fmt())
        self.label.set_label(self.clock.format(self.format))
        if self.clock.is_dead():
            if not self.dead_sound_played:
                self.ui.sounds.play('dead')
                self.dead_sound_played = True
                # need to set it at least only once on refresh
                # further updates can be taken care of on turn changes
                # (hilight())
                self.evbox.set_state(gtk.STATE_SELECTED)

    def hilight(self, active):
        if active:
            if self.clock.is_dead():
                self.evbox.set_state(gtk.STATE_SELECTED)
            else:
                self.evbox.set_state(gtk.STATE_ACTIVE)
        else:
            self.evbox.set_state(gtk.STATE_NORMAL)

    def guess_format(self):
        if self.clock.get_time() < 60000:
            self.format = '%02i:%04.1f'
        else:
            self.format = '%02i:%02d'

    def check_sprint(self):
        # we should move this back to the GameUI
        if self.clock.get_time() < 60000:  # below 60 seconds, kick the ds
            self.ui.loop_timeout = GameclockUI.ms_loop_timeout
            self.timeout_source = gobject.timeout_add(self.ui.loop_timeout,
                                                      self.ui.refresh_current)
            return True
        return False

    def __del__(self):
        self.label.destroy()
        del self.label
