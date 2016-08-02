from hypothesis.utils.conventions import not_set

def accept(f):
    def testExpMethod(self, bexp=not_set, dexp=not_set):
        return f(self, bexp, dexp)
    return testExpMethod
