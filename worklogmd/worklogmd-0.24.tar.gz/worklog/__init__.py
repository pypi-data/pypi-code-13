import sys
from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker
if sys.version_info[0] <= 2:
    from .parsing2 import WorklogLexer, WorklogParser, WorklogListener
else:
    from .parsing import WorklogLexer, WorklogParser, WorklogListener
from .day_stats_walker import DayStatsWalker

def get_day_stats(fname):
    input_file = FileStream(fname)
    lexer = WorklogLexer(input_file)
    stream = CommonTokenStream(lexer)
    parser = WorklogParser(stream)
    tree = parser.wl()

    stats_walker = DayStatsWalker()
    walker = ParseTreeWalker()
    walker.walk(stats_walker, tree)
    stats_walker._save_current_stats()

    return stats_walker.stats
