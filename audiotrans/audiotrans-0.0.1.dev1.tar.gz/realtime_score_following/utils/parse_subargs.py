# -*- coding: utf-8 -*-


def parse_subargs(t):
    """
    Parse sub arguments which formed like:

        '[ foo bar --baz 1 --qux ]'

    and returns like:

        ('foo', [bar], {baz: 1, qux: True})

    Parameters
    ----
    t : Target string of subargs

    Returns
    ----
    Tuple of (first-arg, args-array, kwargs-dict)
    """

    if t.startswith('[ ') and t.endswith(' ]'):
        args = iter(t.split()[1:-1])
        name = next(args)
        n_args = []
        kw_args = {}
        a = next(args, None)
        while a is not None:
            if a.startswith('--'):
                a = a.strip('^--')
                v = next(args, None)
                if v is None:
                    kw_args[a] = True
                    break
                else:
                    kw_args[a] = v
            else:
                n_args.append(a)
            a = next(args, None)
    else:
        return t, [], {}

    return name, n_args, kw_args
