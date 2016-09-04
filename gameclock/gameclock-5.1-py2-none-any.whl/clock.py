# -*- coding: utf-8 -*-
#
# The Gameclock clock engines
#
# This is where the clock engines reside.
#
# (C) Anarcat 2011

import time
import gameclock.i18n
import gettext


class Clock:
    """The main clock engine

    Each clock is an instance of this class. This could be considered
    like a merge between a controler and a model in an MVC
    model. However, this software isn't based on the MVC model in any
    remote way.

    This should be pretty precise and doesn't lag from empirical
    observations (watching the clocks compared to the Gnome clock
    applet)
    """

    def __init__(self, **settings):
        """Setup the clock engine

        The clock is stopped by default and the display is refreshed
        """
        # the time, in miliseconds
        self.time = settings['start_time']
        # 0 if stopped
        self.last_start = 0
        # usually, clocks go backwards, but some games might require
        # it to go other ways
        self.factor = -1
        # a clock is part of a chained list
        if 'next_clock' in settings:
            self.next = settings['next_clock']
        else:
            self.next = None
        self.moves = 0

    def start(self):
        """Start the timer

        This marks the new timestamp and sets the background color
        """
        self.last_start = time.time()

    def stop(self):
        """Stop the timer

        This computes the new cumulatative time based on the start
        timestamp. It resets the timestamp to zero to mark the timer as
        stopped.

        This also resets the event box's color and triggers an update of
        the label.

        XXX: Note that this function takes *some* time to process. This
        time is lost and not given to any participant. Maybe that should
        be fixed for the clock to be really precised, by compensation
        for the duration of the function.

        Another solution would be to create a thread for the Game engine
        """
        if self.last_start:
            self.time = self.get_time()
            self.last_start = 0
            self.moves += 1

    def pause(self):
        """pause/unpause the timer

        this will start the timeer if stopped and stop it if started
        """
        if self.last_start:
            self.stop()
        else:
            self.start()

    def running(self):
        return self.last_start

    def get_time(self):
        """return the current time of the clock in ms"""
        if self.last_start:
            diff = time.time() - self.last_start
        else:
            diff = 0
        return self.time + (self.factor * diff*1000)

    def moves_fmt(self):
        return ngettext("%d move", "%d moves", self.moves) % self.moves

    def is_dead(self):
        return self.get_time() <= 0

    def update(self):
        """Refresh the display of the clock's widget"""
        return self.format()

    suggested_formats = [
        '%02i:%02d',
        '%02i:%04.1f',
        '%i:%02i:%02d',
        '%i:%02i:%04.1f'
        ]

    def format(self, fmt='%02i:%02d'):
        """Format this clock's internal time as a human-readable string.

Can contain 2 or three formatters. If there are only two, hours are
displayed in the minutes."""
        miliseconds = abs(self.get_time())
        if self.get_time() < 0:
            fmt = '-' + fmt
        if fmt.count('%') == 3:
            hours, milliseconds = divmod(miliseconds, 3600000)
        minutes, milliseconds = divmod(miliseconds, 60000)
        seconds = float(milliseconds) / 1000
        if fmt.count('%') == 3:
            return fmt % (hours, minutes, seconds)
        else:
            return fmt % (minutes, seconds)

    def __str__(self):
        """make a better string representation of the objects

        we basically dump all variables and some functions
        """
        return ("  clock engine %s time: %d last: %d "
                "diff: %f dead: %d text: %s next %s"
                % (object.__str__(self),
                   self.time,
                   self.last_start,
                   time.time() - self.last_start,
                   self.is_dead(),
                   self.format(),
                   self.next))


class ChessClock(Clock):
    """A typical Chess clock
    
This clock will stop at the end of your turn, and should represent
fairly faithfully tabletop chess clocks.

A typical setting is 5 minutes each, which is considered to be a
"blitz". 2 minutes is often called "lightning chess".

    """
    # this is just an alias to the base Game class which implements everything
    pass


class FischerChessClock(Clock):
    """A chess clock, as modified by Garry Fischer

This is a regular chess clock with one little twist: every time a
player finishes its turn, he gets extra time. This allows for timed
game that are still fairly interactive, as the player is forced to
move within a certain timeframe.

A typical setting is 2 minutes + 10 seconds delay, which leads to
games of around 10 to 20 minutes.

    """
    delay = 10

    def __init__(self, **settings):
        self.delay = settings['delay']
        del settings['delay']
        Clock.__init__(self, **settings)

    def stop(self):
        """end the turn, fischer style

        this increments the current clock before switching turns as normal
        """
        self.time += self.delay
        Clock.stop(self)


class BoardClock(Clock):
    """A simple clock for general board games.

A player gets a specific amount of time to play his turn, but the
leftover time isn't carried over to the next turn.
    """

    # we need to remember the original time
    default_time = None

    def __init__(self, **settings):
        Clock.__init__(self, **settings)
        self.default_time = settings['start_time']

    def stop(self):
        """override the end_turn function to reset the timers at the end of
        turns"""
        Clock.stop(self)
        self.time = self.default_time


class GoStandardByoyomiClock(Clock):
    """a regular go clock.

    it has a certain time where it behaves like a regular chess clock,
    but then behaves like a board clock after the given time. at that
    point there is a certain number of "byoyomis" of a chosen "delay"
    that moves need to be played within."""

    def __init__(self, **settings):
        self.delay = settings['delay']
        # number of extra time periods, if 0, no time periods are left
        # and the user dies
        # we increment this because we burn the first byoyomi when entering it
        self._byoyomi = settings['byoyomi'] + 1
        self._start_byoyomi = settings['byoyomi']
        Clock.__init__(self, **settings)

    def get_byoyomi(self):
        """look if we are dead and consume a byoyomi if so

should be called as often as necessary to display things
consistently. returns the number of byoyomis used (-1 being regular
game play, 0 being none, 1 being one, etc).
"""
        # can't use our own is_dead, it's subverted by the byoyomi logic
        if Clock.is_dead(self) and not self.is_dead():
            self._byoyomi -= 1
            if self.is_dead():
                self.time = 0
            else:
                # reset the timer only if we didn't blow byoyomi
                self.time = self.delay
            if self.running():
                # reset
                self.start()
        return self._byoyomi

    def set_byoyomi(self, byoyomi):
        self._start_byoyomi = byoyomi
        self._byoyomi = byoyomi + 1

    def is_dead(self):
        return self._byoyomi <= 0

    def is_byoyomi(self):
        return self.get_byoyomi() <= self._start_byoyomi

    def format(self, fmt='%02i:%02d'):
        self.get_byoyomi()
        return Clock.format(self, fmt)

    def stop(self):
        Clock.stop(self)
        if self.is_byoyomi() and not self.is_dead():
            self.time = self.delay

    def moves_fmt(self):
        ret = Clock.moves_fmt(self)
        if self.is_byoyomi():
            ret += ngettext(' %d byoyomi', ' %d byoyomis', self._byoyomi) % self._byoyomi
        if self.is_dead():
            ret += _(' (lost)')
        return ret


class HourglassClock(Clock):
    """Hourglass emulation.

This clock is similar to having an hourglass on a table that is
flipped at the end of each turn.

We do allow each player to start with a certain amonut of time (or
"sand", if you will) on his side, in other words, this is as if the
hourglass was half-empty/half-full when the game starts.

Note that this doesn't make much sense with more than two players...

    """

    def __init__(self, **settings):
        """override the base constructor to make only one clock have an
        initial time

        basically, this is to represent that when you start it, the
        hour glass is empty on one side
        """
        Clock.__init__(self, **settings)

    def start(self):
        """reimplement the start() function altogether

        make sure all the clocks are started and they are in the right
        direction
        """
        Clock.stop(self)
        self.factor = -1
        Clock.start(self)

    def stop(self):
        """reimplement the end_turn function altogether

        we go to the next clock, stop it, reverse its direction and
        start it again
        """
        Clock.stop(self)
        self.factor = 1
        Clock.start(self)
