VERSION = (0, 97, 1)


def get_version():
    return u'.'.join((unicode(num) for num in VERSION))

__version__ = get_version()
