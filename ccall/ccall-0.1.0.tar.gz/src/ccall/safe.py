import functools


#
# Safe input
#
@functools.singledispatch
def safe_input(x):
    """
    Convert input python object into a safe argument to pass to a wrapped C
    function.
    """

    return x


@safe_input.register(str)
def _(x):
    return x.encode('utf8')


#
# Safe output
#
@functools.singledispatch
def safe_output(x):
    """
    Convert resulting object into a safe Python value.
    """

    return x
