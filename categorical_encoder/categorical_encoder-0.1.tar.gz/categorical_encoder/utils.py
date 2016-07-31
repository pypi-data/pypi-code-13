from itertools import chain


def transpose(M, flatten=False):
    """Transpose a matrix M in this particular context

    Keyword arguments:
    M -- square matrix
    flatten -- flatten matrix elements if needed
    """

    if flatten:
        return [
            list(chain.from_iterable([_[i] for _ in M]))
            for i in range(len(M[0]))
        ]

    else:
        return [
            [_[i] for _ in M]
            for i in range(len(M[0]))
        ]
