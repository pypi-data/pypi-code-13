import curses
import cfg
from history import History


class ExTerm(object):

    def __init__(self, title="Title", subtitle="SubTitle", help_function=None):
        self.title = title
        self.subtitle = subtitle
        self.x = 0
        self.y = 0
        self.history = History()
        self.line = []
        self.help_function = help_function

    def show(self):
        curses.wrapper(self.display)

    def display(self, stdscr):
        self.stdscr = stdscr
        self.init_color()
        self.init_curses()
        self.write_line(self.title, False)
        self.write_line(self.subtitle, False)
        self.write_line("")
        self.loop()

    def init_color(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def init_curses(self):
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def loop(self):
        while True:
            line_end = cfg.LEN_START_X + len(self.line)
            try:
                c = self.stdscr.getch()
                if c == cfg.HELP_KEY:  # Help Key
                    self.help_function()
                elif c == curses.KEY_ENTER or c == 10 or c == 13:  # Enter
                    self.write_line("")
                elif c == curses.KEY_BACKSPACE or c == 127:  # Backspace
                    self.backspace()
                elif c == curses.KEY_EXIT or c == cfg.KEY_CTRL_D:  # CTRL-D EXIT
                    break
                else:
                    self.echoc(c)

            except KeyboardInterrupt:
                self.write_line("")
                self.write_line("KeyboardInterrupt")

    def echoc(self, c):
        if 32 <= c <= 126:
            self.stdscr.addch(chr(c))
            self.line.append(c)
            self.x += 1

    def backspace(self):
        if len(self.line) > 0:
            self.x -= 1
            self.stdscr.delch(self.y, self.x)
            self.line = self.line[:-1]

    def start_newline(self, start_prefix):
        self.history.cmds.append(self.line)
        self.stdscr.refresh()
        self.line = []
        if start_prefix:
            self.stdscr.addstr(cfg.START_PREFIX)
            self.x = cfg.LEN_START_X
        else:
            self.x = 0
        self.y += 1

    def write_line(self, msg, start_prefix=True):
        self.stdscr.addstr(msg)
        self.stdscr.addstr("\n")
        self.start_newline(start_prefix)

