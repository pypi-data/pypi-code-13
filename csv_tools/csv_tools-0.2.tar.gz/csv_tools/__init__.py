import bisect
import csv
import functools
import os
from csv import Sniffer
from collections import (Counter, defaultdict, OrderedDict)

from chardet.universaldetector import UniversalDetector
from logbook import Logger

__author__ = "cw-andrews"

logger = Logger()


def file_exists(filepath: str):
    """Return truce if filepath exists and is a file."""

    if os.path.exists(filepath) and os.path.isfile(filepath):
        resp = True
    else:
        resp = False

    return resp


def dir_exists(dirpath: str):
    """Return truce if dirpath exists and is a dir."""

    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        resp = True
    else:
        resp = False

    return resp


def sniff_for_encoding(delimited_file_path: str) -> str:
    """
    Sniff file to try and determine and return encoding
    else returns latin-1.
    """

    encoding_chunks_to_read = 25

    working_filepath = os.path.normpath(delimited_file_path)
    assert file_exists(working_filepath)

    detector = UniversalDetector()

    with open(working_filepath, 'rb') as working_file:
        logger.debug("Sniffing for encoding; '{}'".format(delimited_file_path))
        for chunk in range(encoding_chunks_to_read):
            if not detector.done:
                detector.feed(working_file.read(4096))
            else:
                break
        detector.close()
        if not detector.done:
            encoding = "latin-1"
            logger.debug("Encoding not detected; set to latin-1.")
        else:
            encoding = detector.result['encoding']
            logger.debug("Detected encoding; returning '{}'".format(encoding))

    return encoding


class DialectDetector(object):
    """
    When passed delimited file path will sniff file for dialect and header
    information using specified detection settings for DialectDetector
    instance.
    """

    def __init__(self,
                 poss_delimiters: str = None,
                 bytes_to_read: int = 50000):
        self.spec_char_mapping = {ord(" "): "", ord("?"): "", ord("-"): "_",
                                  ord("/"): "", ord("."): "", ord("$"): "",
                                  ord("&"): "", ord("!"): "", ord("#"): ""}
        self.poss_delimiters = poss_delimiters
        self.bytes_to_read = bytes_to_read

    def sniff_for_dialect(self,
                          delimited_file_path: str,
                          encoding: str='latin-1') -> csv.Dialect:
        """Sniff delimited file and return csv.Dialect."""

        delimited_filepath = os.path.normpath(delimited_file_path)
        assert file_exists(delimited_filepath)

        with open(delimited_filepath, "rt", encoding=encoding) as ftt:
            working_text = ftt.read(self.bytes_to_read)

            logger.debug(
                "Sniffing for dialect; '{}'.".format(delimited_filepath))
            try:
                if self.poss_delimiters:
                    sniffed = Sniffer().sniff(working_text,
                                              delimiters=self.poss_delimiters)
                else:
                    sniffed = Sniffer().sniff(working_text)
                    if len(sniffed.delimiter) != 1 or len(
                            sniffed.quotechar) != 1:
                        poss_delimiters = '|\t,'
                        sniffed = Sniffer().sniff(working_text,
                                                  delimiters=poss_delimiters)
            except csv.Error as csv_error:
                logger.error("There is something wrong with '{}'.".format(
                    delimited_filepath))
                raise csv.Error(csv_error)

        return sniffed

    def sniff_for_headers(self,
                          delimited_file_path: str,
                          delimiter_override: str=None,
                          encoding: str = 'latin-1') -> list:
        """
        Sniff delimited file and return first row if the file has headers else
        list of numbered columns as headers in the form of 'Column' + column #.
        """

        if delimiter_override:
            working_delimiter = delimiter_override
        else:
            working_delimiter = self.sniff_for_dialect(
                delimited_file_path).delimiter

        with open(delimited_file_path, "rt",
                  encoding=encoding) as working_file:
            logger.debug(
                "Creating csv.reader for '{}'.".format(delimited_file_path))
            reader = csv.reader(working_file, delimiter=working_delimiter)

            logger.debug(
                "Sniffing for headers; '{}'".format(delimited_file_path))
            if Sniffer().has_header(working_file.read()):
                working_file.seek(0)
                logger.debug("Headers found; normalizing and returning.")
                return [field.translate(self.spec_char_mapping) for field in
                        next(reader)]
            else:
                working_file.seek(0)
                logger.debug("Headers not found; manufacturing and returning.")
                return ['Column{}'.format(n) for n, _ in
                        enumerate(next(reader), start=1)]


class SchemaEngine(object):
    """
    Engine for data-typing delimited file into field_names, their data type,
    and max length (if applicable).
    """

    def __init__(self):
        self.join_lines_char = "\n"
        self.text_lengths = [25, 35, 50, 75, 125, 150, 175, 225, 255]
        self.longchar_lengths = [500, 1000, 2500, 5000, 10000, 15000, 25000]
        self.filename_fmt = "[{}]"
        self.filetype_fmt = "Format={}"
        self.field_fmt = "Col{0}={1} {2}"

    @staticmethod
    def rounded_len(rounded_lens: list,
                    max_len: int,
                    strict: bool = True) -> int:
        """
        Take list of absolute values (rounded_lens) and use
        bisect to return next largest rounded length.
        """

        rounded_abs_lens = [abs(i) for i in rounded_lens]
        max_len = abs(max_len)

        if strict:
            if max_len > rounded_abs_lens[-1]:
                logger.exception(
                    "ValueError: {} exceeds maximum allowable value."
                    .format(max_len))
                raise ValueError
            else:
                insertion_point = bisect.bisect_left(rounded_abs_lens,
                                                     abs(max_len))
                ret_val = rounded_abs_lens[insertion_point]
        else:
            default_max = rounded_abs_lens[-1]
            n = max_len
            logger.info(
                "{} exceeds max value but strict=False so continuing.".format(
                    n))
            new_max = default_max
            while n > new_max:
                new_max += default_max
            ret_val = new_max

        return ret_val

    @staticmethod
    def build_csv_reader(delimited_file_path: str,
                         file_delimiter: str,
                         file_quotechar: str,
                         file_encoding: str='latin-1') -> list:
        """
        Take delimited file path and yield lines from csv.reader created using
        sniffed encoding and dialect.
        """

        filename = os.path.split(delimited_file_path)[-1]

        logger.debug("Opening working file: '{}'.".format(filename))
        with open(delimited_file_path, "rt", encoding=file_encoding) as wf:
            try:
                csv_reader = csv.reader(wf,
                                        delimiter=file_delimiter,
                                        quotechar=file_quotechar)
            except TypeError as t:
                logger.exception(t)
                raise TypeError

            logger.debug("Skipping headers if exist...")
            if Sniffer().has_header(delimited_file_path):
                next(csv_reader)

            logger.debug("Yielding rows from '{}'.".format(filename))
            yield from csv_reader

    @classmethod
    def _proc_rows_to_dict(cls,
                           headers: list,
                           csv_reader: csv.reader) -> OrderedDict:
        """
        Process delimited file via build_csv_reader into OrderedDict with
        field_names (headers) as keys and values as a list of all tuple values
        produced by process_value_into_tuple.
        """

        logger.debug("Building dict with field names as keys.")
        recs_dict = defaultdict(OrderedDict,
                                {field: list() for field in headers})

        @functools.lru_cache(maxsize=500)
        def det_type(string: str) -> type:
            """
            Take str and determine *type via hierarchy of try-except type
            casting. Return types are int (long), float (double), str (text),
            else None if empty str.
            """

            if string:
                try:
                    int(string)
                except ValueError:
                    try:
                        float(string.replace(",", ""))
                    except ValueError:
                        return str
                    else:
                        return float
                else:
                    return int
            else:
                return None

        @functools.lru_cache(maxsize=500)
        def process_value_into_tuple(value: str) -> tuple:
            """Process str value into tuple of (len(value), type of value)."""

            val = value.strip()
            return len(val), det_type(val)

        logger.debug("Processing records into dict values: Starting...")
        for row in csv_reader:
            for field_name, field_value in zip(headers, row):
                recs_dict[field_name].append(
                    process_value_into_tuple(field_value))
        logger.debug("Processing records: Finished.")

        return recs_dict

    def _proc_str_to_subtype(self, max_len: int) -> str:
        """
        Use max_len to type and return str subclass as well as a rounded max
        length.
        """

        if max_len:
            safe_len = max_len * 2
            if safe_len > self.text_lengths[-1]:
                determined = (
                "LongChar", self.rounded_len(self.longchar_lengths, safe_len))
            else:
                determined = (
                "Text", self.rounded_len(self.text_lengths, safe_len))
            return "{0} Width {1}".format(*determined)
        else:
            return "{0} Width {1}".format("Text",
                                          self.rounded_len(self.text_lengths,
                                                           25))

    def _proc_dict_to_schema_vals(self,
                                  recs_dict: dict,
                                  headers: list) -> list:
        """
        Process dict of lists which are in turn, of tuples, by csv headers
        into list of schema values via branching logic, with certain fields
        (strings) given higher priority.
        """

        logger.debug("Processing dict into schema text: Starting...")
        schema_values = list()

        for key in headers:
            field_lengths, field_types = zip(*recs_dict[key])

            max_len = max(field_lengths)
            unique_types_in_field = set(
                [dtype for dtype in field_types if dtype])

            if str in unique_types_in_field or not unique_types_in_field:
                schema_values.append((key, self._proc_str_to_subtype(max_len)))
            elif float in unique_types_in_field:
                schema_values.append((key, "Double"))
            elif int in unique_types_in_field:
                schema_values.append((key, "Long"))

        logger.debug("Processing dict into schema text: Finished.")
        return schema_values

    def build_schema_str(self,
                         delimited_file_path: str,
                         file_delimiter: str=None,
                         file_quotechar: str=None,
                         file_encoding: str='latin-1') -> str:
        """Process delimited file and return schema string for file passed."""

        def det_filetype(delimiter: str):
            """Take delimiter and return filetype which MSJDB
            recognizes/requires."""

            if delimiter == ",":
                return "CSVDelimited"
            elif delimiter == "\t":
                return "TabDelimited"
            else:
                return "Delimited({})".format(delimiter)

        filename = os.path.split(delimited_file_path)[-1]

        logger.debug("Building schema for '{}'...".format(filename))

        dd = DialectDetector()
        if not file_delimiter:
            file_delimiter = dd.sniff_for_dialect(
                delimited_file_path).delimiter
        if not file_quotechar:
            file_quotechar = dd.sniff_for_dialect(
                delimited_file_path).quotechar
        file_headers = dd.sniff_for_headers(delimited_file_path)
        del dd

        csv_reader = self.build_csv_reader(delimited_file_path,
                                           file_delimiter=file_delimiter,
                                           file_quotechar=file_quotechar,
                                           file_encoding=file_encoding)
        recs_dict = self._proc_rows_to_dict(file_headers, csv_reader)
        schema_values = self._proc_dict_to_schema_vals(recs_dict, file_headers)

        schema_str_list = list()
        logger.debug("Building schema header...")
        schema_str_list.append(self.filename_fmt.format(filename))
        logger.debug("Building filetype...")
        schema_str_list.append(
            self.filetype_fmt.format(det_filetype(file_delimiter)))
        logger.debug("Building data-typed fields...")
        for col_n, value in enumerate(schema_values, start=1):
            field_name, field_type = value
            schema_str = self.field_fmt.format(col_n, field_name, field_type)
            schema_str_list.append(schema_str)

        logger.debug(
            "Schema built; Returning schema for '{}'...".format(filename))
        return self.join_lines_char.join(schema_str_list)


def integrity_check(infile_path: str) -> str:
    """
    Take filepath and report on the number of columns detected per line,
    extra quotechars, etc. Helps to detect problems in source files which may
    cause issues when creating schema files and indicator for whether file
    will need preprocessor.
    """

    working_filepath = os.path.join(infile_path)
    assert file_exists(working_filepath)

    has_headers = True
    dialect = csv.Dialect
    dialect.delimiter = '|'
    dialect.quotechar = '"'

    quotes_per_line = list()
    columns_per_line = list()
    output = list()

    output.append("Filename: '{}'".format(os.path.split(working_filepath)[-1]))
    output.append("Detected Field Delimiter: [{}]".format(dialect.delimiter))
    output.append("Detected Text Delimiter: [{}]".format(dialect.quotechar))
    output.append("Checking for even # of Text Delimiters on every line...")

    with open(working_filepath, "rt", encoding='latin-1') as infile:
        reader = infile.readlines()
        uneven_tdelimiter_list = list()

        for n, line in enumerate(reader, start=1):
            quotes = Counter(line)[dialect.quotechar]
            quotes_per_line.append(quotes)

            if quotes % 2 != 0:
                uneven_tdelimiter_list.append(
                    "Line {} = {} [{}]'s".format(n, quotes, dialect.quotechar))

        if uneven_tdelimiter_list:
            output.append(
                "FAILED: lines with uneven number of text delimiters detected.")
            output.append("PROBLEM LINES:")
            output.append("\n".join(uneven_tdelimiter_list))
            output.append("TEXT DELIMITER DISPERSAL:")
            quote_counter = Counter(quotes_per_line)
            quote_dispersal = list()
            for n in quote_counter.most_common():
                quote_dispersal.append(
                    "{} lines = {} text delimiters.".format(n[1], n[0]))
            output.append("\n".join(quote_dispersal))
        else:
            output.append(
                "PASSED: NO lines with uneven text delimiter count found.")

    output.append(
        "Checking for the same number of columns/fields on every line...")
    with open(working_filepath, "rt", encoding='latin-1') as infile:
        reader = csv.reader(infile, dialect=dialect)
        headers = next(reader)
        if not has_headers:
            reader.seek(0)

        header_column_count = len(headers)

        output.append(
            "Columns in header/first row = {}".format(header_column_count))

        problem_line_numbers = list()
        bad_column_count = list()

        for n, line in enumerate(reader):
            column_count = len(line)
            columns_per_line.append(column_count)

            if header_column_count != column_count:
                bad_column_count.append(
                    "Line {} = {} columns/fields.".format(n, column_count))
                problem_line_numbers.append(str(n))

    if not problem_line_numbers:
        output.append("PASSED: All lines have consistent column/field count.")
    else:
        output.append(
            "FAILED: lines with different number of columns/fields detected.")
        output.append("PROBLEM LINES:")
        output.append("\n".join(bad_column_count))
        output.append("COLUMN/FIELD DISPERSAL:")
        column_counter = Counter(columns_per_line)
        column_dispersal = list()
        for n in column_counter.most_common():
            column_dispersal.append("{} lines = {} columns/fields.".format(
                n[1], n[0]))
        output.append("\n".join(column_dispersal))
    return "\n".join(output)
