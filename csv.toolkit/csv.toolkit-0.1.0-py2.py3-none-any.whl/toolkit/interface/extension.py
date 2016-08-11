#
# Copyright (c) 2016, Michael Conroy
#


class Extension(object):
    """ Extension class to define tooling implementations """
    class __metaclass__(type):  # noqa: N801
        def __new__(cls, name, bases, members):
            cls = type.__new__(cls, name, bases, members)
            return cls

    @classmethod
    def enabled(cls):
        """
        Return ``True`` for complete tooling implementations and ``False``
        for abstract and mixin classes.
        """

        return (cls is not Extension)

    @classmethod
    def all(cls):
        """
        Returns a list of all tool implementations of tooling interface.
        """

        # Find all subcasses of `cls`.
        subclasses = [cls]
        # Used to weed out duplicates (due to diamond inheritance).
        seen = set([cls])
        idx = 0
        while idx < len(subclasses):
            base = subclasses[idx]
            for subclass in base.__subclasses__():
                if subclass not in seen:
                    subclasses.append(subclass)
                    seen.add(subclass)
            idx += 1
        # Filter out abstract classes and disabled implementations
        implementations = []
        for subclass in subclasses:
            implementations.append(subclass)
        return [implementation
                for implementation in implementations
                if implementation.enabled()]

    @classmethod
    def signature(cls):
        """
        Returns a (unique) identifier of the tooling implementation.

        Impelementations must override this method.
        """

        raise NotImplementedError("%s.signature()" % cls)

    @classmethod
    def mapped(cls, package=None):
        """
        Returns a dictionary mapping extension signatures to extensions.
        """
        mapping = {}
        for extension in cls.all():
            signature = extension.signature()
            assert signature not in mapping, \
                "%s and %s have identical signatures: %r" \
                % (mapping[signature], extension, signature)
            mapping[signature] = extension
        return mapping
