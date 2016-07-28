"""
          .        .--.   _..._
        .'|        |__| .'     '.   .--./)
    .| <  |        .--..   .-.   . /.''\\
  .' |_ | |        |  ||  '   '  || |  | |
.'     || | .'''-. |  ||  |   |  | \`-' /
'--.  .-'| |/.'''. \|  ||  |   |  | /("'`
  |  |  |  /    | ||  ||  |   |  | \ '---.
  |  |  | |     | ||__||  |   |  |  /'""'.\
  |  '.'| |     | |    |  |   |  | ||     ||
  |   / | '.    | '.   |  |   |  | \'. __//
  `'-'  '---'   '---'  '--'   '--'  `'---'
"thing" database - github/itslukej
"""
from .closed import ClosedDict
from .wrapper import Wrapper
from . import encoder

try:
    import anydbm
except ImportError:
    import dbm as anydbm

class thing(Wrapper):
    def __init__(self, filename, flag="c"):
        database = anydbm.open(filename, flag)
        self.filename=filename
        self.flags = flag
        Wrapper.__init__(self, database)
    def sync(self):
        if type(self.dict) is not ClosedDict:
            for key, entry in self.cache.items():
                self.dict[key] = encoder.enpickle(entry)
            self.cache = {}
            #if hasattr(self.dict, 'save'):
            #    self.dict.save()
    def close(self):
        if type(self.dict) is not ClosedDict:
            self.sync()
            self.dict.close()
            self.dict = ClosedDict()
    def __repr__(self):
        return "thingdb({0})".format(self.filename)