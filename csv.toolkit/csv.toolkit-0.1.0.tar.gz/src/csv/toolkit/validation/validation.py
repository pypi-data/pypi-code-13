#
# Copyright (c) 2016, Michael Conroy
#


import csv
import six
import collections


from ..logger import SimpleLogger
from exceptions import ValidationException
from validators import EmptyVal


__all__ = (
    'DEFAULT_DELIMITER',
    'DEFAULT_VALIDATOR',
    'BaseFileValidator',
    'SimpleCSVFileValidator',
)


class BaseFileValidator(object):
    """
    Base class for CSV validators.

    Subclass this class to create a CSV validator by specifying the validators,
    delimeter, default validator, and check duplicate headers attributes.

    Implementations must specify the ``validators`` attribute and define the
    ``validate`` function.
    """

    validators = NotImplemented
    delimeter = NotImplemented
    default_validator = NotImplemented
    check_duplicate_headers = NotImplemented
    logger = NotImplemented

    Result = collections.namedtuple('Result', 'validation, log')

    def __init__(self, source):
        self.failures = collections.defaultdict(
            lambda: collections.defaultdict(list)  # Need a callable to nest
        )
        self.missing_validators = None
        self.missing_fields = None
        self.source = source

        # Set validation to default validators if no validators provided
        self.validators.update({
            field: [self.default_validator()]
            for field, value in six.iteritems(self.validators) if not value
        })

    def __call__(self):
        validation = self.validate()
        log = self.log
        return self.Result(validation, log)

    @property
    def log(self):
        outlog = self.logger.logs
        self.logger.clear()
        return outlog

    def validate(self):
        """
        CSV validation tooling.

        Implementations must override this method.
        """

        raise NotImplementedError("%s.validate()" % self.__class__.__name__)


class ValidationLogger(SimpleLogger):
    """ Validation logging """

    pass


DEFAULT_DELIMITER = ','
DEFAULT_VALIDATOR = EmptyVal
DEFAULT_DISPLAY_LIMIT = 30


class SimpleCSVFileValidator(BaseFileValidator):
    """ Validates CSV files """

    validators = {}
    delimiter = DEFAULT_DELIMITER
    default_validator = DEFAULT_VALIDATOR
    check_duplicate_headers = True
    logger = ValidationLogger()

    def set_validators(self, headers):
        self.validators = {header: [] for header in headers}

    def validate(self):  # noqa: MC0001
        self.logger.log("\nValidating {}(source={})".format(
            self.__class__.__name__, self.source))

        reader = csv.DictReader(self.source.open(), delimiter=self.delimiter)

        # Check for fieldnames
        if not reader.fieldnames:
            self.logger.log("Source CSV has no field names")
            return False

        # Check for duplicate column names
        if self.check_duplicate_headers and \
                (len(reader.fieldnames) != len(set(reader.fieldnames))):
            duplicates = find_duplicates_by_idx(reader.fieldnames)
            self.logger.log('Found duplicate column headers:')
            for header, idxs in six.iteritems(duplicates):
                locations = ", ".join([str(idx) for idx in idxs])
                self.logger.log('  Header: ' + header +
                                ', columns: ' + locations)

        # Check for missing validators
        self.missing_validators = set(reader.fieldnames) - set(self.validators)
        if self.missing_validators:
            self.logger.log("Missing validators for:")
            log_missing(self.missing_validators, self.logger)
            return False

        # Check for missing fields
        self.missing_fields = set(self.validators) - set(reader.fieldnames)
        if self.missing_fields:
            self.logger.log("Missing expected fields:")
            log_missing(self.missing_fields, self.logger)
            return False

        # Validation algorithm
        for line, row in enumerate(reader):
            for field_name, field in six.iteritems(row):
                for validator in self.validators[field_name]:
                    try:
                        validator.validate(field, row=row)
                    except ValidationException as exc:
                        self.failures[field_name][line].append(exc)
                        validator.failure_count += 1

        # Log validation failures
        if self.failures:
            self.logger.log("Failed validation\n")
            log_failures(self.failures, self.source, self.logger)
            log_validator_failures(self.validators, self.logger)
            return False
        else:
            self.logger.log("Successful validation\n")
            return True


def log_failures(failures, source, logger):
    for field_name, field_failure in six.iteritems(failures):
        logger.log("\nFailure on field: \"{}\":".format(field_name))
        for i, (row, errors) in enumerate(six.iteritems(field_failure)):
            logger.log("  {}:{}".format(source, row))
            for error in errors:
                logger.log("    {}".format(error))


def log_validator_failures(validators, logger):
    for field_name, validators_list in six.iteritems(validators):
        for validator in validators_list:
            if validator.fails():
                logger.log(
                    "  {} failed {} time(s) on field: '{}'".format(
                        validator.__class__.__name__, validator.failure_count,
                        field_name))
                invalid = list(validator.fails())
                display = ["'{}'".format(field)
                           for field in invalid[:DEFAULT_DISPLAY_LIMIT]]
                hidden = len(invalid[DEFAULT_DISPLAY_LIMIT:])
                logger.log(
                    "    Invalid fields: [{}]".format(", ".join(display)))
                if hidden:
                    logger.log(
                        "    ({} more suppressed)".format(hidden))


def log_missing(missing_items, logger):
    logger.log(
        "{}".format("\n".join(["  '{}': [],".format(field)
                               for field in sorted(missing_items)]) + "\n"))


def find_duplicates_by_idx(inlist):
    """
    Finds duplicate entries in a list and returns their index in the list.

    :param inlist: List with possible duplicates
    :type list: list
    :returns: Dict of value names and idxs
    :rtype: dictionary
    """
    assert isinstance(inlist, list), 'Function parameter must be of type list'
    enumed_list = collections.defaultdict(list)
    for idx, value in enumerate(inlist):
        enumed_list[value].append(idx)
    indexed_duplicates = {
        value: idxs
        for value, idxs in six.iteritems(enumed_list)
        if len(idxs) > 1
    }
    return indexed_duplicates
