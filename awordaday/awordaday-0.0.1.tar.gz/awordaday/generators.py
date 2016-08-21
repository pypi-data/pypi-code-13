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
