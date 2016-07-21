def single(iterable, default=None):
    """
    Ensures only a single item exists in an iterable and returns it.
​
    :param iterable: the iterable to search for a single element
    :return: Returns the only item in the iterable.
    :raises SequenceError: Raised when the iterable does not have exactly one item.
    """
    if len(iterable) == 0:
        raise SequenceError(message='Expected exactly one item but the iterable contained none.')
    if len(iterable) > 1:
        raise SequenceError(message='Expected exactly one item but the iterable contained more than one.')
    return next(iter(iterable))


def single_or_default(iterable, default_value=None):
    """
    Ensures no more than a single item exists in an iterable and returns it if it exists, otherwise it returns a
    default value.
​
    :param iterable: the iterable to search for a single element
    :param default_value: the value to return if the iterable is empty.
    :return: Returns the only item in the iterable or the default_value if the iterable is empty
    :raises SequenceError: Raised when the iterable does not have exactly one item.
    """
    if len(iterable) == 0:
        return default_value
    if len(iterable) > 1:
        raise SequenceError(message='Expected one or fewer items but the iterable contained more than one.')
    return next(iter(iterable))


def first(sequence):
    """
    Ensures at least a single item exists in a sequence and returns the first one.
​
    :param sequence: the sequence to search for the first element
    :return: Returns the first item in the sequence.
    :raises SequenceError: Raised when the sequence does not have any items.
    """
    if len(sequence) == 0:
        raise SequenceError(message='Expected at least one item but the sequence contained none.')
    return sequence[0]


def first_or_default(sequence, default_value=None):
    """
    Returns the first item in a sequence it if it exists, otherwise it returns a default value.
​
    :param sequence: the sequence to search for a single element
    :param default_value: the value to return if the sequence is empty.
    :return: Returns the first item in the sequence or the default_value if the sequence is empty
    :raises SequenceError: Raised when the sequence is not valid.
    """
    if len(sequence) == 0:
        return default_value
    return sequence[0]


def last(sequence):
    """
    Ensures at least a single item exists in a sequence and returns the last one.
​
    :param sequence: the sequence to search for the last element
    :return: Returns the last item in the sequence.
    :raises SequenceError: Raised when the sequence does not have any items.
    """
    if len(sequence) == 0:
        raise SequenceError(message='The sequence contained no elements.')
    return sequence[len(sequence)-1]


def last_or_default(sequence, default_value=None):
    """
    Returns the last item in a sequence it if it exists, otherwise it returns a default value.
​
    :param sequence: the sequence to search for a single element
    :param default_value: the value to return if the sequence is empty.
    :return: Returns the last item in the sequence or the default_value if the sequence is empty
    :raises SequenceError: Raised when the sequence is not valid.
    """
    if len(sequence) == 0:
        return default_value
    return sequence[len(sequence)-1]


def distinct(sequence):
    """
    Returns a set of the distinct members in a sequence.
​
    :param sequence: the sequence to search for distinct members.
    :return: Returns a set if distinct members in the sequence.
    """
    seen = set()
    for item in sequence:
        if item not in seen:
            seen.add(item)
            yield item


class SequenceError(Exception):
    """"""
    def __init__(self, *args, message='An error was encountered while attempting to perform a mapping.', **kwargs):
        """
        Creates an instance of the MappingError Exception.
​
        :param args: Arguments to be passed to the base Exception.
        :param message: A message to display to the user when the error is raised.
        :param kwargs: Key word arguments to be passed to the base Exception.
        """
        super(Exception, self).__init__(self, message, *args, **kwargs)
        self._message = message

    @property
    def message(self):
        """A message describing the nature or the error."""
        return self._message