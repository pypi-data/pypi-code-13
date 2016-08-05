class Buffer():
    def __init__(self):
        self._lines = []

    def store(self, line):
        self._lines.append(line)

    @property
    def lines(self):
        return self._lines

    @property
    def contents(self):
        return "\n".join(self._lines)
