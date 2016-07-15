from argparse import ArgumentParser, _AppendAction


class OverrideAppendAction(_AppendAction):
    """
    An append action that only uses the default list when no values are given.

    See: https://bugs.python.org/issue16399.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        if values and (
                getattr(namespace, self.dest, self.default) is self.default):
            setattr(namespace, self.dest, [])
        super().__call__(parser, namespace, values, option_string)


class OverrideAppendArgumentParser(ArgumentParser):
    """
    Registers OverrideAppendAction as oappend.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register('action', 'oappend', OverrideAppendAction)
