#
# Copyright (c) 2016, Michael Conroy
#


from six import StringIO, BytesIO, string_types, binary_type
from exceptions import LoaderException


__all__ = (
    'Loader',

    'StringLoader',

    'LocalFileLoader',
)


class Loader(object):
    """ Base class for file loaders """

    loader = NotImplemented
    loader_args = None
    loader_kwargs = None

    def __init__(self, source):
        """ Initializes loader mechanism """
        self.source = source

    def open(self):
        """
        Opens a file object using the ``loader`` parameter and returns it

        Implementations must override this method.
        """

        raise NotImplementedError("%s.open()" % self.__class__.__name__)

    def __repr__(self):
        """
        Implementations may override this method to produce pretty output.
        """

        return "{}('{}')".format(self.__class__.__name__, type(self.source))


class StringLoader(Loader):
    """ Loads strings """

    loader = StringIO

    def open(self):
        try:
            string = self.source if isinstance(self.source, string_types) \
                else self.loader(self.source.read())
            return string
        except Exception as exc:
            raise LoaderException(
                'Unable to read string. Got:\n{}'.format(str(exc))
            )

    def __repr__(self):
        if hasattr(self.source, 'name'):
            descriptor = self.source.name
        else:
            descriptor = type(self.source)
        return "{}('{}')".format(self.__class__.__name__, descriptor)


class LocalFileLoader(Loader):
    """ Loads from a local file path """

    loader = open
    loader_args = ['r', ]
    loader_kwargs = {}

    def open(self):
        try:
            with self.loader(self.source, *self.loader_args,
                             **self.loader_kwargs) as f:
                return f.readlines()
        except Exception as exc:
            raise LoaderException(
                'Unable to load local file. Got:\n{}'.format(str(exc))
            )

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, str(self.source))
