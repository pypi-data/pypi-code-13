"""
    hybrid_attributes
    ~~~~~~~~~~~~~~~~~

    :copyright: 2016 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst
"""


__version__ = '0.1.0'
__version_info__ = (0, 1, 0)


class hybrid_property:
    """
    A `property` like descriptor that gives you the ability to produce values
    when accessed on a class.

    :param fget:
        A function that is called with the instance or class the property is
        accessed on, the result will be returned as attribute.

    :param fset:
        A function that will be called when a value is assigned to the
        attribute on an instance.

    :param fdel:
        A function that is called when the attribute is deleted on an instance.

    :param fcget:
        A function that is called when the attribute is accessed on a class,
        with that class as argument.

        Use this when you need to do something different, depending on whether
        the attribute is accessed on a class or an instance.

    If any of these functions are missing, an :exc:`AttributeError` will be
    raised when a user performs an operation that would otherwise lead to such
    a function being called.

    Instead of passing all arguments directly, you should use decorators to
    define the different functions::

        class SomeClass:
            @hybrid_property
            def attribute(self):
                return self._attribute

            @attribute.classgetter
            def attribute(cls):
                return 'SomeClass.attribute was accessed'

            @attribute.setter
            def attribute(self, value):
                self._attribute = value

            @attribute.deleter
            def attribute(self, value):
                del self._attribute
    """
    def __init__(self, fget=None, fset=None, fdel=None, fcget=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.fcget = fcget

    def __get__(self, instance, owner):
        if instance is None:
            if self.fcget is None and self.fget is None:
                raise AttributeError('unreadable attribute')
            return (self.fcget or self.fget)(owner)
        else:
            if self.fget is None:
                raise AttributeError('unreadable attribute')
            return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)

    def getter(self, fget):
        """
        Returns a new `hybrid_property` instance with `fget` set to the given
        function.
        """
        return self._copy(fget=fget)

    def setter(self, fset):
        """
        Returns a new `hybrid_property` instance with `fset` set to the given
        function.
        """
        return self._copy(fset=fset)

    def deleter(self, fdel):
        """
        Returns a new `hybrid_property` instance with `fdel` set to the given
        function.
        """
        return self._copy(fdel=fdel)

    def classgetter(self, fcget):
        """
        Returns a new `hybrid_property` instance with `fcget` set to the given
        function.
        """
        return self._copy(fcget=fcget)

    def _copy(self, fget=None, fset=None, fdel=None, fcget=None):
        return self.__class__(
            fget=self.fget if fget is None else fget,
            fset=self.fset if fset is None else fset,
            fdel=self.fdel if fdel is None else fdel,
            fcget=self.fcget if fcget is None else fcget
        )


class hybrid_method:
    """
    A descriptor that binds functions to whatever object, class or instance, it
    has been accessed on. This allows you to use a function as an instance
    method and a class method at the same time.

    :param function:
        A function that is bound to the class or instance and returned, when
        the attribute is accessed on a class or instance respectively.

    :param class_function:
        A function that is bound to the class, instead of `function`, when the
        attribute is accessed on a class.

        Use this when you need different behavior when the method is called on
        a class.

    Instead of passing all arguments directly, you should use the `classmethod`
    decorator to define the `class_function`::

        class SomeClass:
            @hybrid_method
            def spam(self):
                return 'called on a SomeClass instance'

            @spam.classmethod
            def spam(cls):
                return 'called on SomeClass'
    """
    def __init__(self, function, class_function=None):
        self._function = function
        self._class_function = class_function

    def __get__(self, instance, owner):
        if instance is None:
            clsmethod = classmethod(self._class_function or self._function)
            return clsmethod.__get__(instance, owner)
        return self._function.__get__(instance, owner)

    def classmethod(self, class_function):
        """
        Returns a new `hybrid_method` instance with `class_function` set to the
        given function.
        """
        return self.__class__(self._function, class_function)
