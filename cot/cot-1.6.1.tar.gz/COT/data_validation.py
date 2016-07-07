#!/usr/bin/env python
#
# data_validation.py - Helper libraries to validate data sanity
#
# September 2013, Glenn F. Matthews
# Copyright (c) 2013-2016 the COT project developers.
# See the COPYRIGHT.txt file at the top-level directory of this distribution
# and at https://github.com/glennmatthews/cot/blob/master/COPYRIGHT.txt.
#
# This file is part of the Common OVF Tool (COT) project.
# It is subject to the license terms in the LICENSE.txt file found in the
# top-level directory of this distribution and at
# https://github.com/glennmatthews/cot/blob/master/LICENSE.txt. No part
# of COT, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE.txt file.

"""Various helpers for data sanity checks.

**Exceptions**

.. autosummary::
  :nosignatures:

  InvalidInputError
  ValueMismatchError
  ValueUnsupportedError
  ValueTooLowError
  ValueTooHighError

**Functions**

.. autosummary::
  :nosignatures:

  canonicalize_helper
  canonicalize_ide_subtype
  canonicalize_nic_subtype
  canonicalize_scsi_subtype
  check_for_conflict
  device_address
  mac_address
  match_or_die
  natural_sort
  no_whitespace
  non_negative_int
  positive_int
  to_string
  validate_int

**Constants**

.. autosummary::
  NIC_TYPES
"""

import xml.etree.ElementTree as ET
import re


def to_string(obj):
    """Get string representation of an object, special-case for XML Element."""
    if ET.iselement(obj):
        return ET.tostring(obj)
    else:
        return str(obj)


def natural_sort(l):
    """Sort the given list "naturally" rather than in ASCII order.

    E.g, "10" comes after "9" rather than between "1" and "2".

    See also http://nedbatchelder.com/blog/200712/human_sorting.html

    :param list l: List to sort
    :return: Sorted list
    """
    def convert(text):
        """Convert number strings to ints, leave other strings as text."""
        return int(text) if text.isdigit() else text

    def alphanum_key(key):
        """Split the key into a list of [text, int, text, int, ...]."""
        return [convert(c) for c in re.split('([0-9]+)', key)]

    # Sort based on alphanum_key
    return sorted(l, key=alphanum_key)


def match_or_die(first_label, first, second_label, second):
    """Make sure "first" and "second" are equal or raise an error.

    :param str first_label: Descriptive label for :attr:`first`
    :param first: First object to compare
    :param str second_label: Descriptive label for :attr:`second`
    :param second: Second object to compare
    :raise ValueMismatchError: if ``first != second``
    """
    if first != second:
        raise ValueMismatchError("{0} {1} does not match {2} {3}"
                                 .format(first_label,
                                         to_string(first),
                                         second_label,
                                         to_string(second)))


def canonicalize_helper(label, user_input, mappings, re_flags=0):
    """Try to find a mapping of input to output.

    :param str label: Label to use in any error raised
    :param str user_input: User-provided string
    :param list mappings: List of ``(expr, canonical)`` pairs for mapping.
    :param re_flags: ``re.IGNORECASE``, etc. if desired
    :returns: The canonical string
    :raise ValueUnsupportedError: If no ``expr`` in ``mappings`` matches
      ``input``.
    """
    if user_input is None or user_input == "":
        return None
    for (expr, canonical) in mappings:
        if re.match(expr, user_input, flags=re_flags):
            return canonical
    raise ValueUnsupportedError(label, user_input, [c for (_, c) in mappings])


def canonicalize_ide_subtype(subtype):
    """Try to convert the given IDE controller string to a canonical form.

    :param str subtype: User-provided string
    :returns: The canonical string, one of:

      - ``PIIX4``
      - ``virtio``

    :raise ValueUnsupportedError: If the canonical string cannot be determined
    """
    return canonicalize_helper("IDE controller subtype", subtype,
                               [
                                   ("piix4", 'PIIX4'),
                                   ("virtio", 'virtio'),
                               ],
                               re.IGNORECASE)

_NIC_MAPPINGS = [
    ("e1000e", 'E1000e'),
    ("e1000", 'E1000'),
    ("pcnet32", 'PCNet32'),
    ("virtio", 'virtio'),
    ("vmxnet *3", 'VMXNET3'),
]

NIC_TYPES = [m[1] for m in _NIC_MAPPINGS]
"""List of NIC type strings recognized as canonical."""


def canonicalize_nic_subtype(subtype):
    """Try to convert the given NIC subtype string to a canonical form.

    :param str subtype: User-provided string
    :returns: The canonical string, one of :data:`NIC_TYPES`

    :raise ValueUnsupportedError: If the canonical string cannot be determined

    .. seealso::
       :meth:`COT.platforms.GenericPlatform.validate_nic_type`
    """
    return canonicalize_helper("NIC subtype", subtype,
                               _NIC_MAPPINGS, re.IGNORECASE)


def canonicalize_scsi_subtype(subtype):
    """Try to convert the given SCSI controller string to a canonical form.

    :param str subtype: User-provided string
    :returns: The canonical string, one of:

      - ``buslogic``
      - ``lsilogic``
      - ``lsilogicsas``
      - ``virtio``
      - ``VirtualSCSI``

    :raise ValueUnsupportedError: If the canonical string cannot be determined
    """
    return canonicalize_helper("SCSI controller subtype", subtype,
                               [
                                   ("bus *logic", 'buslogic'),
                                   ("lsi *logic *sas", 'lsilogicsas'),
                                   ("lsi *logic", 'lsilogic'),
                                   ("virtio", 'virtio'),
                                   ("virtual *scsi", 'VirtualSCSI'),
                               ],
                               re.IGNORECASE)


def check_for_conflict(label, li):
    """Make sure the list does not contain references to more than one object.

    :param str label: Descriptive label to be used if an error is raised
    :param list li: List of object references (which may include ``None``)
    :raises ValueMismatchError: if references differ
    :returns: the object or ``None``
    """
    obj = None
    for i, obj1 in enumerate(li):
        if obj1 is None:
            continue
        for obj2 in li[(i+1):]:
            if obj2 is not None and obj1 != obj2:
                raise ValueMismatchError(
                    "Found multiple candidates for the {0}: "
                    "\n{1}\n...and...\n{2}\nPlease correct or clarify "
                    "your search parameters."
                    .format(label, to_string(obj1), to_string(obj2)))
        obj = obj1
    return obj


def mac_address(string):
    """Parser helper function for MAC address arguments.

    Validate whether a string is a valid MAC address.
    Recognized formats are:

    * xx:xx:xx:xx:xx:xx
    * xx-xx-xx-xx-xx-xx
    * xxxx.xxxx.xxxx

    :param string: String to validate
    :raise InvalidInputError: if string is not a valid MAC address
    :return: Validated string(with leading/trailing whitespace stripped)
    """
    string = string.strip()
    if not (re.match(r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$", string) or
            re.match(r"([0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2}$", string) or
            re.match(r"([0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}$", string)):
        raise InvalidInputError("'{0}' is not a valid MAC address"
                                .format(string))
    # TODO - reformat string to a consistent output style?
    return string


def device_address(string):
    """Parser helper function for device address arguments.

    Validate string is an appropriately formed device address such as '1:0'.

    :param str string: String to validate
    :raise InvalidInputError: if string is not a well-formatted device address
    :return: Validated string (with leading/trailing whitespace stripped)
    """
    string = string.strip()
    if not re.match(r"\d+:\d+$", string):
        raise InvalidInputError("'{0}' is not a valid device address"
                                .format(string))
    return string


def no_whitespace(string):
    """Parser helper function for arguments not allowed to contain whitespace.

    :param str string: String to validate
    :raise InvalidInputError: if string contains internal whitespace
    :return: Validated string (with leading/trailing whitespace stripped)
    """
    string = string.strip()
    if len(string.split()) > 1:
        raise InvalidInputError("'{0}' contains invalid whitespace"
                                .format(string))
    return string


def validate_int(string,
                 min=None, max=None,  # pylint: disable=redefined-builtin
                 label="input"):
    """Parser helper function for validating integer arguments in a range.

    :param str string: String to convert to an integer and validate
    :param int min: Minimum valid value (optional)
    :param int max: Maximum valid value (optional)
    :param str label: Label to include in any errors raised
    :return: Validated integer value
    :raise ValueUnsupportedError: if :attr:`string` can't be converted to int
    :raise ValueTooLowError: if value is less than :attr:`min`
    :raise ValueTooHighError: if value is more than :attr:`max`
    """
    try:
        i = int(string)
    except ValueError:
        raise ValueUnsupportedError(label, string, "integer")
    if min is not None and i < min:
        raise ValueTooLowError(label, i, min)
    if max is not None and i > max:
        raise ValueTooHighError(label, i, max)
    return i


def non_negative_int(string):
    """Parser helper function for integer arguments that must be 0 or more.

    Alias for :func:`validate_int` setting :attr:`min` to 0.
    """
    return validate_int(string, min=0)


def positive_int(string):
    """Parser helper function for integer arguments that must be 1 or more.

    Alias for :func:`validate_int` setting :attr:`min` to 1.
    """
    return validate_int(string, min=1)


# Some handy exception and error types we can throw
class ValueMismatchError(ValueError):
    """Values which were expected to be equal turned out to be not equal."""

    pass


class InvalidInputError(ValueError):
    """Miscellaneous error during validation of user input."""

    pass


class ValueUnsupportedError(InvalidInputError):
    """An unsupported value was provided.

    :ivar value_type: descriptive string
    :ivar actual_value: invalid value that was provided
    :ivar expected_value: expected (valid) value or values (item or list)
    """

    def __init__(self, value_type, actual, expected):
        """Create an instance of this class."""
        self.value_type = value_type
        self.actual_value = actual
        self.expected_value = expected
        super(ValueUnsupportedError, self).__init__(str(self))

    def __str__(self):
        """Human-readable string representation."""
        return ("Unsupported value '{0}' for {1} - expected {2}"
                .format(self.actual_value, self.value_type,
                        self.expected_value))


class ValueTooLowError(ValueUnsupportedError):
    """A numerical input was less than the lowest supported value.

    :ivar value_type: descriptive string
    :ivar actual_value: invalid value that was provided
    :ivar expected_value: minimum supported value
    """

    def __str__(self):
        """Human-readable string representation."""
        return ("Value '{0}' for {1} is too low - must be at least {2}"
                .format(self.actual_value, self.value_type,
                        self.expected_value))


class ValueTooHighError(ValueUnsupportedError):
    """A numerical input was higher than the highest supported value.

    :ivar value_type: descriptive string
    :ivar actual_value: invalid value that was provided
    :ivar expected_value: maximum supported value
    """

    def __str__(self):
        """Human-readable string representation."""
        return ("Value '{0}' for {1} is too high - must be at most {2}"
                .format(self.actual_value, self.value_type,
                        self.expected_value))
