import itertools


class FileBaseQuoteGenerator(object):
    def __init__(self, input_file):
        self.f = open(input_file, 'r')

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            return next(self.f).strip()
        except StopIteration:
            self.f.seek(0)
            return next(self)


class SimpleGenerator(object):
    def __init__(self, iterator):
        self.iterator = itertools.cycle(iterator)

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        return str(next(self.iterator)).strip()
