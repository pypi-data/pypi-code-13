from pyfunk.combinators import compose, curry
from pyfunk.collections import fmap as cfmap


@curry
def fmap(fn, f):
    '''
    Generic version of fmap.
    @sig fmap :: Functor f => (a -> b) -> f a -> f b
    '''
    return f.fmap(fn) if hasattr(f, 'fmap') else cfmap(fn, f)


@curry
def chain(fn, c):
    '''
    Generic version of chain
    @sig chain :: Chain c => (a -> c b) -> c a -> c b
    '''
    return c.chain(fn)


@curry
def ap(fof, fn, f):
    '''
    Generic ap
    @sig ap :: Applicative a, Functor f => (t -> a t) -> (x -> y) -> f x -> a y
    '''
    return fof(fn).ap(f)


def ccompose(*fns):
    '''
    Composes functions that produce Chains
    @sig mcompose :: Chain c => (y -> c z)...(x -> c y) -> (x -> c z)
    '''
    last = fns[-1:]
    rest = tuple(list(map(chain, fns[:-1])))
    chained = rest + last
    return compose(*chained)


@curry
def liftA2(fn, f1, f2):
    '''
    Generic version of liftA2
    @sig ap :: Functor f => (x -> y -> z) -> f x -> f y -> a z
    '''
    return f1.fmap(fn).ap(f2)


@curry
def liftA3(fn, f1, f2, f3):
    '''
    Generic version of liftA3
    @sig ap :: Functor f => (w -> x -> y -> z) f v -> f x -> f y -> a z
    '''
    return f1.fmap(fn).ap(f2).ap(f3)


from pyfunk.monads.base import Monad  # noqa
from pyfunk.monads.identity import Identity  # noqa
from pyfunk.monads.const import Const  # noqa
from pyfunk.monads.either import Left, Right, ftry, cata  # noqa
from pyfunk.monads.io import IO  # noqa
from pyfunk.monads.maybe import Maybe, maybe, maybify  # noqa
from pyfunk.monads.task import Task  # noqa
