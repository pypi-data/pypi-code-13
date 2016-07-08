class delegate_to:
    """
    Property that delegates attribute access to a different attribute.
    """

    def __init__(self, delegate_to, readonly=False):
        self.delegate_to = delegate_to
        self.readonly = readonly

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        owner = getattr(obj, self.delegate_to)
        try:
            attr = self._name
        except AttributeError:
            attr = self._get_name(cls)
        return getattr(owner, attr)

    def __set__(self, obj, value):
        if self.readonly:
            raise AttributeError

        owner = getattr(obj, self.delegate_to)
        try:
            attr = self._name
        except AttributeError:
            attr = self._get_name(type(obj))
        setattr(owner, attr, value)

    def _get_name(self, cls):
        for k in dir(cls):
            v = getattr(cls, k)
            if v is self:
                return k
        raise RuntimeError('not a member of class')


def delegate_ro(delegate_to):
    """
    A read-only version of delegate_to()
    """

    def __init__(delegate_to):
        super().__init__(delegate_to, True)


class lazy:
    """
    Defines an attribute that is initialized as first usage rather than at
    instance creation.

    This can be used either to simplify the __init__ method or avoid or delay
    potentially expensive computations.

    Example
    -------

    >>> class Computation:
    ...     @lazy
    ...     def answer(self):
    ...         print('the answer')
    ...         return 42


    The .answer attribute is initialized only at first access.

    >>> deep_thought = Computation()
    >>> answer = deep_thought.answer
    the answer
    >>> print(answer)
    42

    Other than that, it behaves just like any python attribute.

    >>> other = Computation()
    >>> other.answer = 3.1415
    >>> other.answer
    3.1415
    """

    def __init__(self, method):
        self.method = method
        self.__name__ = getattr(method, '__name__', None)

    def __get__(self, obj, cls):
        if obj is None:
            return self

        result = self.method(obj)
        try:
            attr_name = self._attr
        except AttributeError:
            attr_name = self.get_attribute_name(cls)

        setattr(obj, attr_name, result)
        return result

    def get_attribute_name(self, cls):
        """Inspect live object for some attributes."""

        try:
            if getattr(cls, self.__name__) is self:
                return self.__name__
        except AttributeError:
            pass

        for attr in dir(cls):
            method = getattr(cls, attr, None)
            if method is self:
                self._attr = attr
                return attr

        raise TypeError('lazy accessor not found in %s' % cls.__name__)
