"""
    test_hybrid_attributes
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2016 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
import inspect

import pytest

from hybrid_attributes import hybrid_method, hybrid_property


class TestHybridProperty:
    """
    Tests for the `hybrid_property` descriptor.
    """

    def test_get_on_instance(self):
        class Foo:
            @hybrid_property
            def spam(self):
                assert isinstance(self, Foo)
                return 'spam'

        assert Foo().spam == 'spam'

    def test_get_on_class(self):
        class Foo:
            @hybrid_property
            def spam(self):
                assert self is Foo
                return 'spam'

        assert Foo.spam == 'spam'

    def test_get_without_fget(self):
        class Foo:
            spam = hybrid_property()

        with pytest.raises(AttributeError) as exc_info:
            Foo().spam

        assert len(exc_info.value.args) == 1
        assert exc_info.value.args[0] == 'unreadable attribute'

    def test_get_without_fget_on_class(self):
        class Foo:
            spam = hybrid_property()

        with pytest.raises(AttributeError) as exc_info:
            Foo.spam

        assert len(exc_info.value.args) == 1
        assert exc_info.value.args[0] == 'unreadable attribute'

    def test_set_on_instance(self):
        class Foo:
            def _set_spam(self, value):
                assert isinstance(self, Foo)
                self._spam = value

            spam = hybrid_property(fset=_set_spam)

        foo = Foo()
        foo.spam = 1
        assert foo._spam == 1

    def test_set_without_fset(self):
        class Foo:
            spam = hybrid_property()

        foo = Foo()
        with pytest.raises(AttributeError) as exc_info:
            foo.spam = 1

        assert len(exc_info.value.args) == 1
        assert exc_info.value.args[0] == "can't set attribute"

    def test_delete_on_instance(self):
        class Foo:
            def _delete_spam(self):
                assert isinstance(self, Foo)
                self._delete_was_called = True

            spam = hybrid_property(fdel=_delete_spam)

        foo = Foo()
        del foo.spam
        assert foo._delete_was_called

    def test_delete_without_fdel(self):
        class Foo:
            spam = hybrid_property()

        foo = Foo()
        with pytest.raises(AttributeError) as exc_info:
            del foo.spam

        assert len(exc_info.value.args) == 1
        assert exc_info.value.args[0] == "can't delete attribute"

    def test_get_with_fcget(self):
        class Foo:
            def _get_spam(self):
                assert self is Foo
                return 'spam'

            spam = hybrid_property(fcget=_get_spam)

        assert Foo.spam == 'spam'

    def test_get_with_fcget_has_priority(self):
        class Foo:
            def _get_spam(self):
                assert isinstance(self, Foo)
                return 1

            def _cget_spam(self):
                assert self is Foo
                return 2

            spam = hybrid_property(fget=_get_spam, fcget=_cget_spam)

        assert Foo().spam == 1
        assert Foo.spam == 2

    def test_getter(self):
        class Foo:
            p = hybrid_property()

            @p.getter
            def spam(self):
                return 'spam'

        assert Foo.spam == 'spam'

    def test_setter(self):
        class Foo:
            p = hybrid_property()

            @p.setter
            def spam(self, value):
                self._spam = value

        foo = Foo()
        foo.spam = 1
        assert foo._spam == 1

    def test_deleter(self):
        class Foo:
            p = hybrid_property()

            @p.deleter
            def spam(self):
                self._spam_is_deleted = True

        foo = Foo()
        del foo.spam
        assert foo._spam_is_deleted

    def test_classgetter(self):
        class Foo:
            p = hybrid_property()

            @p.classgetter
            def spam(self):
                return 'spam'

        assert Foo.spam == 'spam'


class TestHybridMethod:
    """
    Tests for the `hybrid_method` descriptor.
    """

    def test_is_bound_method_on_instance(self):
        class Foo:
            @hybrid_method
            def spam(self):
                assert isinstance(self, Foo)
                return 'spam'

        foo = Foo()
        assert inspect.ismethod(foo.spam)
        assert foo.spam() == 'spam'

    def test_is_bound_method_on_class(self):
        class Foo:
            @hybrid_method
            def spam(self):
                assert self is Foo
                return 'spam'

        assert inspect.ismethod(Foo.spam)
        assert Foo.spam() == 'spam'

    def test_different_implementation_on_class(self):
        class Foo:
            def _get_spam(self):
                assert isinstance(self, Foo)
                return 'instance'

            def _get_class_spam(cls):
                assert cls is Foo
                return 'class'

            spam = hybrid_method(_get_spam, _get_class_spam)

        assert Foo.spam() == 'class'
        assert Foo().spam() == 'instance'

    def test_classmethod(self):
        class Foo:
            @hybrid_method
            def spam(self):
                return 'instance'

            @spam.classmethod
            def spam(cls):
                return 'class'

        assert Foo.spam() == 'class'
        assert Foo().spam() == 'instance'
