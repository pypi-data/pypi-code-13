from numbers import Real
from time import perf_counter


class Timer(Real):
    """
    Simple timing context manager.

    Implements all abstract methods of numbers.Real.
    """
    def __enter__(self):
        self.entry_time = perf_counter()
        return self

    def __exit__(self, *args, **kwargs):
        self.exit_time = perf_counter()

    def __add__(self, other):
        return float(self).__add__(other)

    def __radd__(self, other):
        return float(self).__radd__(other)

    def __neg__(self):
        return float(self).__neg__()

    def __pos__(self):
        return float(self).__pos__()

    def __sub__(self, other):
        return float(self).__sub__(other)

    def __rsub__(self, other):
        return float(self).__rsub__(other)

    def __mul__(self, other):
        return float(self).__mul__(other)

    def __rmul__(self, other):
        return float(self).__rmul__(other)

    def __truediv__(self, other):
        return float(self).__truediv__(other)

    def __rtruediv__(self, other):
        return float(self).__rtruediv__(other)

    def __pow__(self, exponent):
        return float(self).__pow__(exponent)

    def __rpow__(self, base):
        return float(self).__rpow__(base)

    def __abs__(self):
        return float(self).__abs__()

    def __eq__(self, other):
        return float(self).__eq__(other)

    def __float__(self):
        return float(self.exit_time - self.entry_time)

    def __trunc__(self):
        return float(self).__trunc__()

    def __floor__(self):
        return float(self).__floor__()

    def __ceil__(self):
        return float(self).__ceil__()

    def __round__(self, ndigits=None):
        return float(self).__round__(ndigits=ndigits)

    def __floordiv__(self, other):
        return float(self).__floordiv__(other)

    def __rfloordiv__(self, other):
        return float(self).__rfloordiv__(other)

    def __mod__(self, other):
        return float(self).__mod__(other)

    def __rmod__(self, other):
        return float(self).__rmod__(other)

    def __lt__(self, other):
        return float(self).__lt__(other)

    def __le__(self, other):
        return float(self).__le__(other)

    def __str__(self):
        return str(float(self))

    def __repr__(self):
        return repr(float(self))

    def __format__(self, format_spec):
        return float(self).__format__(format_spec)

    def __hash__(self):
        return hash(float(self))
