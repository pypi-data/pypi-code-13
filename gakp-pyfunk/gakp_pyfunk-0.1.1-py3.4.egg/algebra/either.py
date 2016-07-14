from pyfunk.algebra import Algebra as _Algebra
from pyfunk.combinators import curry as _curry


def ftry(fn):
    '''
    Equivalent to try-except using Either monad
    @sig ftry :: Either e => (* -> a) -> (* -> e b a)
    '''
    def trier(*args, **kwargs):
        try:
            Right.of(fn(*args, **kwargs))
        except Exception as e:
            Left.of(e)
    return trier


@_curry
def cata(f, g, e):
    '''
    Extracts the values from either for transformation there f is for
    Left and g for Right
    @sig cata :: Either a b => (a -> c) -> (b -> c) -> Either a b -> c
    '''
    if isinstance(e, Left):
        return f(e._value)
    elif isinstance(e, Right):
        return g(e._value)


class Left(_Algebra):

    def fmap(self, fn):
        '''
        Does nothing
        @sig fmap :: Left l => (a -> b) -> l a
        '''
        return self

    def join(self):
        '''
        Returns the same left monad
        @sig join :: Left l => _ -> l a
        '''
        return self


class Right(_Algebra):
    pass
