
def dtens(*terms):
    """ The tensor product, defined for states represented as dicts """
    output = defaultdict(complex)
    if len(terms) == 0:
        return {}
    for q in it.product(*(t.items() for t in terms)):
        keys, amps = zip(*q)
        newkey = tuple(sorted(reduce(add, keys)))
        output[newkey] = np.prod(amps)
    return output


def dinner(a, b):
    """ Inner product of states represented as dicts """
    return sum([np.conj(a[key]) * b[key] for key in set(a.keys() + b.keys())])

