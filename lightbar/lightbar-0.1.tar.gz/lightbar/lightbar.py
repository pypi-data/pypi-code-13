import time


class LightBar:
    def __init__(self, gntr, block="░", width=100):
        self.source = gntr
        self.block = block
        self.width = width

    def _good_value(self, i):
        return isinstance(i, int) and i > 0 and i <= 100

    def __call__(self):
        while True:
            try:
                i = next(self.source)
                if not self._good_value(i):
                    raise ValueError("Expecting integer between 1 and 100.")
            except StopIteration:
                print("")
                break
            s = self.block * int(i / 100 * self.width)
            print("-{}%-: {}".format(i, s), end="\r")


if __name__ == '__main__':
    def progress():
        for i in range(1, 101):
            yield i
            time.sleep(0.1)

    LightBar(progress())()
    LightBar(progress(), block="▓", width=20)()
    LightBar(progress(), width=40)()
