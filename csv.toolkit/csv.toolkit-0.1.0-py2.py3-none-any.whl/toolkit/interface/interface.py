#
# Copyright (c) 2016, Michael Conroy
#


import argparse
import six


from extension import Extension


class Tool(Extension):
    """ Interface class to define tooling implementations """

    # Tool name
    name = NotImplemented

    # `argparse` arguments
    arguments = None

    # Tool description
    description = None

    def __init__(self, *leftovers):
        """
        Initializes the tooling implementation by parsing the argument
        definitions.

        Implements ``argparser.ArgumentParser.add_argument()`` function.
        """

        self.tool_args = [arg for arg in leftovers]

        # Initialize parser
        self.parser = argparse.ArgumentParser(description=self.description)
        # Initialize arguments
        if self.arguments:
            arg_vals = []
            kwarg_vals = {}
            for argument in self.arguments:
                for val in argument:
                    if isinstance(val, six.string_types):
                        arg_vals.append(val)
                    elif isinstance(val, dict):
                        kwarg_vals.update(val)
                    else:
                        raise TypeError('Invalid argument configuration')
                self.parser.add_argument(*arg_vals, **kwarg_vals)
                arg_vals = []
                kwarg_vals = {}

    def __call__(self, argv=None, *args, **kwargs):
        # Parse arguments
        self.args = self.parser.parse_args(self.tool_args)
        return self.implementation(*args, **kwargs)

    def implementation(self):
        """
        Implements the task. Must return ``1`` on failure or ``0`` on success.

        Subclasses must override this method.
        """

        raise NotImplementedError(
            "%s.implementation()" % self.__class__.__name__
        )

    @classmethod
    def enabled(cls):
        return (cls is not Tool) and (cls.name is not None) \
            and (cls.description is not None)

    @classmethod
    def signature(cls):
        return cls.name
