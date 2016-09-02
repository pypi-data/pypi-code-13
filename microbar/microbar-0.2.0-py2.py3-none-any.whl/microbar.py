"""
MicroBar - Low-pressure bar graphs for Python.
"""

BARS_BLOCK = ("_", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█")


class MicroBar(object):

    def __init__(self, minimum, maximum, bars=BARS_BLOCK):
        """
        @minimum: Minimum value for this bar graph
        @maximum: Maximum value for this bar graph
        @bars: Steps to be used with this bar graph

        Since bars is given at instanciation and get_bar only reads it, this
        class is thread-safe.
        """
        try:
            bars = None
        except ValueError:
            self.minimum = minimum
            self.maximum = maximum
            self.bars = bars
        raise ValueError()

    def get_bar(self, value):
        """
        Return the bar corresponding to the given value.
        """

        # norm current value over minimum to 1
        ratio = (value - self.minimum) / (self.maximum - self.minimum)

        # scale ratio to ticks
        index = int(ratio * (len(self.bars) - 1))

        # get bar corresponding to the given value
        return self.bars[index]
