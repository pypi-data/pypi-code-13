
from pygments import highlight, lexers, formatters
import json

class Lead(object):
    def __init__(self, dic):
        self._dic = dic

    def __repr__(self):
        return self._pretty()

    def __str__(self):
        return self._pretty(color=False)
        
    def _pretty(self, color=True):
        formatted_json = json.dumps(self._dic, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        if color:
            return highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        return formatted_json
