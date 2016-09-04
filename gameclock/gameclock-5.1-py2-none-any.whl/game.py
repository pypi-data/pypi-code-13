# -*- coding: utf-8 -*-
#
# The gameclock game engines
#
# This is where the game engines reside.
#
# (C) Anarcat 2011

import re
import inspect

import gameclock.clock


def valid_game(cls):
    return inspect.isclass(cls) and not cls.__name__.startswith('Abstract')


def enumerate_games():
    classes = inspect.getmembers(gameclock.game, valid_game)
    return sorted(classes,
                  lambda x, y: cmp(_(x[1].nice_name()),
                                   _(y[1].nice_name())),
                  reverse=True)


class AbstractGame:
    """the game engine
    
    this regroups clocks and handles turn switches

    this is an abstract class, it needs to be extended to do anything.
    """

    # default settings for new games, overridable in the constructor
    # or the properties of the object after creation
    players = 2

    # either name the class after the clock (e.g. ChessClock ->
    # ChessGame) or define this to associate this game with a specific
    # clock
    clock_type = None

    def __init__(self, **settings):
        # import settings as object attributes
        for key, val in settings.iteritems():
            setattr(self, key, val)
        # export back those attributes as settings to the clock
        for key in vars(self.__class__):
            settings[key] = getattr(self, key)

        settings['start_time'] = self.time

        # this finds the class name of the clock we want, either set
        # explicitely in the game class attribute or by guessing the
        # name from the game class
        clock_type = self.__class__.clock_type or \
                     getattr(gameclock.clock,
                             self.__class__.__name__.split('Game')[0] +
                             'Clock')

        # the clock engines
        p = clock_type(**settings)  # the last clock (next_clock = None)
        # this goes backwards
        for i in range(self.players-1):
            settings['next_clock'] = p
            p = clock_type(**settings)  # the previous clock
        # the clocks in the game
        #
        # in chess there are two clocks, but there can be more. this
        # is simply a list
        self.first_clock = self.cur_clock = p

    def resize(self, players):
        clock_type = self.__class__.clock_type or \
                     getattr(gameclock.clock,
                             self.__class__.__name__.split('Game')[0]
                             + 'Clock')
        settings = {}
        for key in vars(self.__class__):
            settings[key] = getattr(self, key)
        settings['start_time'] = self.time
        settings['next'] = None

        p = self.first_clock
        p.next = None
        for i in range(players-1):
            if p.next is None:
                p.next = clock_type(**settings)
            p = p.next
        self.players = players

    def copy(self):
        """return a new game object similar to this one"""
        settings = {}
        for key in vars(self.__class__):
            settings[key] = getattr(self, key)
        return self.__class__(**settings)

    def start(self):
        """start the game
        
        this basically starts the clock
        """
        self.cur_clock.start()

    def move(self):
        """make a move, that is, end the current turn
        
        this is the handler for the main button. it will stop the
        active clock and start the other and switch the active clock
        """
        self.cur_clock.stop()
        # XXX: we might lose a few ms here
        self.next()
        self.cur_clock.start()

    def pause(self):
        """pause the game
        
        this just pauses the current clock

        returns true if the current clock is paused
        """
        self.cur_clock.pause()
        return not self.cur_clock.running()

    def next(self):
        """change the current clock to the next one"""
        self.cur_clock = self.cur_clock.next or self.first_clock

    def alive(self):
        def _check_alive(clock):
            return not clock.is_dead()
        return self.foreach(_check_alive)

    def dead(self):
        return not self.alive()

    def running(self):
        return self.cur_clock.running()

    def foreach(self, function):
        """run the given function on all clock objects

return true if all calls return true"""
        ret = True
        p = self.first_clock
        while p:
            ret = function(p) and ret
            p = p.next
        return ret

    def set_time(self, time):
        """reset the time of all clocks to the given time"""
        self.time = time

        # this is actually almost as long as the original non-foreach
        # function, but allows for testing the API
        def h(p):
            p.time = time
        self.foreach(h)

    def __str__(self):
        """make a better string representation of the objects
        
        we basically dump all variables and some functions
        """
        return "  game engine %s\n  \n  first %s\n  current %s" % \
            (object.__str__(self), self.first_clock, self.cur_clock)

    @classmethod
    def nice_name(cls):
        """this funky bit splits the class name on capital letters and gets
        rid of the last entry ('Game')
        """
        return ' '.join(filter(lambda x: x, re.split('([A-Z][a-z]*)',
                                                     cls.__name__))[:-1])


class AbstractDelayGame(AbstractGame):
    """games that have a concept of a delay"""

    delay = None  # abstract class

    def set_delay(self, delay):
        def s(clock):
            clock.delay = delay
        self.foreach(s)


class AbstractGoGame(AbstractDelayGame):
    """go games have a delay, but also a byoyomi"""

    byoyomi = None  # abstract class

    def set_byoyomi(self, byoyomi):
        def s(clock):
            clock.set_byoyomi(byoyomi)
        self.foreach(s)

    @classmethod
    def nice_name(cls):
        return _('Go: %s') % ' '.join(filter(lambda x: x,
                                             re.split('([A-Z][a-z]*)',
                                                      cls.__name__))[1:-1])


class AbstractChessGame(AbstractGame):
    clock_type = gameclock.clock.ChessClock

    @classmethod
    def nice_name(cls):
        return _('Chess: %s') % re.split('([A-Z][a-z]*)', cls.__name__)[1]


class RegularChessGame(AbstractChessGame):
    """A regular chess game of 60 minutes per player, with no increment."""
    time = 60 * 60 * 1000


class QuickChessGame(AbstractChessGame):
    """A quick 15 minutes per player chess game, no increment."""
    time = 15 * 60 * 1000


class LightningChessGame(AbstractChessGame):
    """A very fast chess game, 5 minutes per player no increment."""
    time = 5 * 60 * 1000


class FischerChessGame(AbstractDelayGame):
    """A delay timing style used for chess and designed by Bobby Fischer. Everytime the player makes a move, a delay is added to the clock. Defaults: 2 minutes per player, 10 second increment, results in a reasonably short chess game."""
    
    time = 2 * 60 * 1000
    delay = 10 * 1000

    @classmethod
    def nice_name(cls):
        return _('Chess: Fischer')


class BoardGame(AbstractGame):
    """A regular board game. A clock goes down until time runs out. The counter is reset at every move. Default is to give 2 minutes per move."""
    time = 2 * 60 * 1000


class HourglassGame(AbstractGame):
    """Behave like an hourglass: the clock goes down on one side and up on the other, 60 seconds by default."""
    time = 60 * 1000

    def start(self):
        """override the start routine to make sure clocks are properly started"""
        p = self.first_clock
        while p:
            if p == self.cur_clock:
                p.start()
            else:
                p.stop()
            p = p.next


class GoStandardByoyomiGame(AbstractGoGame):
    """A standard or "japanese" Go counter. A clock counts down until its time runs out and then enters overtime. Once in overtime the player has a specific number of overtime periods (or "Byo-yomi") to play. If the player moves within the chosen delay, the clock's time reverts to the top of the period and no periods are lost. If the player does not move within the period, the next period begins and the period count is reduced by 1. A player loses when his/her clock runs out of time and no more periods remain."""
    time = 30 * 60 * 1000  # 30 minutes
    byoyomi = 5  # 5 spare delays
    delay = 60 * 1000  # 60 seconds
