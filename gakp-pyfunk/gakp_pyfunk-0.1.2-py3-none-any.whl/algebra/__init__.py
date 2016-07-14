from pyfunk.combinators import compose as _compose, curry as _curry


@_curry
def fmap(fn, f):
    '''
    Generic version of fmap.
    @sig fmap :: Functor f => (a -> b) -> f a -> f b
    '''
    return f.fmap(fn)


@_curry
def freduce(f, fn, x):
    '''
    Generic freduce
    @sig freduce :: Foldable f => (a -> b -> c) -> a -> c
    '''
    return f.freduce(fn, x)


@_curry
def chain(fn, c):
    '''
    Generic version of chain
    @sig chain :: Chain c => (a -> c b) -> c a -> c b
    '''
    return c.chain(fn)


@_curry
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
    rest = list(map(fns[:-1], chain))
    return _compose(*(rest + (last,)))


@_curry
def liftA2(fn, f1, f2):
    '''
    Generic version of liftA2
    @sig ap :: Functor f => (x -> y -> z) -> f x -> f y -> a z
    '''
    return f1.fmap(fn).ap(f2)


@_curry
def liftA3(fn, f1, f2, f3):
    '''
    Generic version of liftA3
    @sig ap :: Functor f => (w -> x -> y -> z) f v -> f x -> f y -> a z
    '''
    return f1.fmap(fn).ap(f2).ap(f3)


@_curry
def sequence(fof, ms):
    '''
    Sequences a list of monads using the given applicative
    @sig sequence :: Applicative a, Monad m => (t -> a t) -> [m] -> a [m]
    '''
    return fof(list(map(freduce, ms)))


from pyfunk.algebra.algebra import Algebra  # noqa
from pyfunk.algebra.container import Container  # noqa
from pyfunk.algebra.either import Left, Right, ftry, cata  # noqa
from pyfunk.algebra.io import IO  # noqa
from pyfunk.algebra.maybe import Maybe, maybe, maybify  # noqa
from pyfunk.algebra.task import Task  # noqa
