from itertools import chain, combinations

from django.conf import settings
from django.test import RequestFactory

# Whether or not to include a fake `Request` in the global context.
REQUEST = getattr(settings, 'IXC_COMPRESSOR_REQUEST', True)

# A sequence of key/value tuples to be included in every generated context.
GLOBAL_CONTEXT = getattr(settings, 'IXC_COMPRESSOR_GLOBAL_CONTEXT', [])

# A sequence of key/value tuples, every combination of which will be combined
# with the global context when generating contexts.
OPTIONAL_CONTEXT = getattr(settings, 'IXC_COMPRESSOR_OPTIONAL_CONTEXT', [])


def get_compress_offline_context():
    """
    Combine global context and every combination of optional contexts to
    generate offline contexts.
    """
    global_context = {}
    if REQUEST:
        global_context.update({
            'request': RequestFactory().get('/'),
        })
    global_context.update(GLOBAL_CONTEXT)
    for optional_context in powerset(OPTIONAL_CONTEXT):
        context = {}
        context.update(global_context)
        context.update(optional_context)
        yield context


# See: https://docs.python.org/2/library/itertools.html#recipes
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
