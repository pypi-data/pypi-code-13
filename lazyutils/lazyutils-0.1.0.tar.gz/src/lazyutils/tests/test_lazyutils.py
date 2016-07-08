import pytest

from lazyutils import delegate_to


def test_delegate_to_property():
    class A:
        bar = delegate_to('foo')

    class B:
        pass

    x = A()
    x.foo = B()
    x.foo.bar = 42

    assert x.bar == 42