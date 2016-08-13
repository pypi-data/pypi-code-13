__version__ = '0.0.4'


def flake8ext(f):
    f.name = 'flake8_meiqia'
    f.version = __version__
    f.skip_on_py3 = False
    if not hasattr(f, 'off_by_default'):
        f.off_by_default = False
    return f
