"""
MicroBar - Low-pressure bar graphs for Python.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

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
        if not type(bars) is tuple:
            raise TypeError('Parameter "bars" must be of type tuple.')

        if not type(minimum) in [int, float]:
            raise TypeError(
                'Parameter "minimum" must be of type "int" or "float".')

        if not type(maximum) in [int, float]:
            raise TypeError(
                'Parameter "maximum" must be of type "int" or "float".')

        if not minimum < maximum:
            raise ValueError(
                'Parameter "minimum" must be smaller than "maximum".')

        self.minimum = minimum
        self.maximum = maximum
        self.bars = bars

    def get_bar(self, value):
        """
        Return the bar corresponding to the given value.
        """

        # norm current value over minimum to 1
        ratio = (value - self.minimum) / (self.maximum - self.minimum)

        # scale ratio to ticks
        index = int(round(ratio * (len(self.bars) - 1)))

        # get bar corresponding to the given value
        return self.bars[index]
