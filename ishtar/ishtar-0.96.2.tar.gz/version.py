VERSION = (0, 96, 2)


def get_version():
    return u'.'.join((unicode(num) for num in VERSION))

__version__ = get_version()
