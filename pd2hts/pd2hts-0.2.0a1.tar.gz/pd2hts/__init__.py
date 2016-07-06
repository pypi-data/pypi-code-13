from configparser import ParsingError
from datetime import datetime
from io import SEEK_CUR, SEEK_END, SEEK_SET, UnsupportedOperation

import numpy as np
import pandas as pd
from textbisect import text_bisect_left, text_bisect_right


class BacktrackableFile(object):

    def __init__(self, fp):
        self.fp = fp
        self.line_number = 0
        self.next_line = None

    def readline(self):
        if self.next_line is None:
            self.line_number += 1
            result = self.fp.readline()
        else:
            result = self.next_line
            self.next_line = None
        return result

    def backtrack(self, line):
        self.next_line = line

    def read(self, size=None):
        return self.fp.read() if size is None else self.fp.read(size)

    def __getattr__(self, name):
        return getattr(self.fp, name)


class FilePart(object):
    """A wrapper that views only a subset of the wrapped filelike object.

    When it is created, three mandatory parameters are passed: a filelike
    object, startpos and endpos. This wrapper then acts as a filelike object of
    size endpos+1-startpos, which views the part of the wrapped object between
    startpos and endpos.
    """

    def __init__(self, stream, startpos, endpos):
        self.startpos = startpos
        self.endpos = endpos
        self.stream = stream
        if self.stream.tell() < self.startpos:
            self.stream.seek(self.startpos)
        if self.stream.tell() > self.endpos + 1:
            self.stream.seek(0, SEEK_END)

    def read(self, size=-1):
        max_available_size = self.endpos + 1 - self.stream.tell()
        size = min(size, max_available_size)
        if size == -1:
            size = max_available_size
        return self.stream.read(size)

    def readline(self, size=-1):
        max_available_size = self.endpos + 1 - self.stream.tell()
        size = min(size, max_available_size)
        return self.stream.readline(size)

    def seek(self, offset, whence=SEEK_SET):
        if whence == SEEK_SET:
            if offset < 0:
                raise ValueError("negative seek position {}".format(offset))
            targetpos = self.startpos + offset
            if targetpos > self.endpos + 1:
                targetpos = self.endpos + 1
            self.stream.seek(targetpos)
            # It might seem more reasonable to return targetpos -
            # self.startpos, but we choose to do the same thing Python does in
            # other cases; if you do f.seek(VERY_LARGE), it returns VERY_LARGE,
            # even if it is larger than the size of the file.
            return offset
        elif whence == SEEK_CUR:
            # Do nothing by simply calling the wrapped (which requires that
            # offset be zero).
            return self.stream.seek(offset, SEEK_CUR)
        elif whence == SEEK_END:
            if offset != 0:
                return UnsupportedOperation(
                    "can't do nonzero cur-relative seeks")
            return self.stream.seek(self.endpos)
        else:
            assert(False)

    def tell(self):
        return self.stream.tell() - self.startpos

    def __getattr__(self, name):
        return getattr(self.stream, name)


def _key(x):
    return x.split(',')[0]


def read(f, start_date=None, end_date=None):
    # Determine start_date and end_date as ISO8601 strings
    start_date = '0001-01-01 00:00' if start_date is None else start_date
    end_date = '9999-12-31 00:00' if end_date is None else end_date
    start_date = start_date.strftime('%Y-%m-%d %H:%M') \
        if isinstance(start_date, datetime) else start_date
    end_date = end_date.strftime('%Y-%m-%d %H:%M') \
        if isinstance(end_date, datetime) else end_date

    # Determine the subset of the file that is of interest
    lo = f.tell()
    endpos = text_bisect_right(f, end_date, lo=lo, key=_key) - 1
    startpos = text_bisect_left(f, start_date, lo=lo, key=_key)
    f2 = FilePart(f, startpos, endpos)

    # Read it
    return pd.read_csv(f2, parse_dates=[0], names=('date', 'value', 'flags'),
                       usecols=('date', 'value', 'flags'), index_col=0,
                       header=None, converters={'flags': lambda x: x},
                       dtype={'value': np.float64, 'flags': str})


def write(df, f):
    if df.empty:
        return
    float_format = '%f'
    if hasattr(df, 'precision') and df.precision is not None:
        if df.precision >= 0:
            float_format = '%.{}f'.format(df.precision)
        else:
            float_format = '%.0f'
            datacol = df.columns[0]
            m = 10 ** (-df.precision)
            df[datacol] = np.rint(df[datacol] / m) * m
    df.to_csv(f, float_format=float_format, header=False, mode='wb',
              line_terminator='\r\n', date_format='%Y-%m-%d %H:%M')


class _ReadFile:

    def __call__(self, f):
        f = BacktrackableFile(f)

        # Check if file contains headers
        first_line = f.readline()
        f.backtrack(first_line)
        if isinstance(first_line, bytes):
            first_line = first_line.decode('utf-8-sig')
        has_headers = not first_line[0].isdigit()

        # Read file, with its headers if needed
        self.meta = {}
        if has_headers:
            self.read_meta(f)
        result = read(f)
        result.__dict__.update(self.meta)

        return result

    def read_meta(self, f):
        """Read the headers of a file in file format and place them in the
        self.meta dictionary.
        """
        if not isinstance(f, BacktrackableFile):
            f = BacktrackableFile(f)

        try:
            (name, value) = self.read_meta_line(f)
            while name:
                name = (name == 'nominal_offset' and 'timestamp_rounding' or
                        name)
                name = (name == 'actual_offset' and 'timestamp_offset' or name)
                method_name = 'get_{}'.format(name)
                method = getattr(self, method_name, None)
                if method:
                    method(name, value)
                name, value = self.read_meta_line(f)
                if not name and not value:
                    break
        except ParsingError as e:
            e.args = e.args + (f.line_number,)
            raise

    def get_unit(self, name, value):
        self.meta[name] = value
    get_title = get_unit
    get_timezone = get_unit
    get_variable = get_unit

    def get_time_step(self, name, value):
        minutes, months = self.read_minutes_months(value)
        self.meta[name] = '{},{}'.format(minutes, months)
    get_timestamp_rounding = get_time_step
    get_timestamp_offset = get_time_step

    def get_interval_type(self, name, value):
        self.meta[name] = value.lower()
        if self.meta[name] not in ('sum', 'average', 'maximum', 'minimum',
                                   'vector_average'):
            raise ParsingError(("Invalid interval type"))

    def get_precision(self, name, value):
        try:
            self.meta[name] = int(value)
        except ValueError as e:
            raise ParsingError(e.args)

    def get_comment(self, name, value):
        if 'comment' in self.meta:
            self.meta['comment'] += '\n'
        else:
            self.meta['comment'] = ''
        self.meta['comment'] += value

    def get_location(self, name, value):
        if 'location' not in self.meta:
            self.meta['location'] = {}
        try:
            items = value.split()
            self.meta['location']['abscissa'] = float(items[0])
            self.meta['location']['ordinate'] = float(items[1])
            self.meta['location']['srid'] = int(items[2])
        except (IndexError, ValueError):
            raise ParsingError("Invalid location")

    def get_altitude(self, name, value):
        if 'location' not in self.meta:
            self.meta['location'] = ''
        try:
            items = value.split()
            self.meta['location']['altitude'] = float(items[0])
            self.meta['location']['asrid'] = int(items[1]) \
                if len(items) > 1 else None
        except (IndexError, ValueError):
            raise ParsingError("Invalid altitude")

    def read_minutes_months(self, s):
        """Return a (minutes, months) tuple after parsing a "M,N" string.
        """
        try:
            (minutes, months) = [int(x.strip()) for x in s.split(',')]
            return minutes, months
        except Exception:
            raise ParsingError(('Value should be "minutes, months"'))

    def read_meta_line(self, f):
        """Read one line from a file format header and return a (name, value)
        tuple, where name is lowercased. Returns ('', '') if the next line is
        blank. Raises ParsingError if next line in f is not a valid header
        line."""
        line = f.readline()
        if isinstance(line, bytes):
            line = line.decode('utf-8-sig')
        name, value = '', ''
        if line.isspace():
            return (name, value)
        if line.find('=') > 0:
            name, value = line.split('=', 1)
            name = name.rstrip().lower()
            value = value.strip()
        name = '' if any([c.isspace() for c in name]) else name
        if not name:
            raise ParsingError("Invalid file header line")
        return (name, value)


read_file = _ReadFile()


class _WriteFile:

    def __call__(self, df, f, version=4):
        self.version = version
        self.df = df
        self.f = f
        self.write_meta()
        self.f.write('\r\n')
        write(self.df, self.f)

    def write_meta(self):
        if self.version == 2:
            self.f.write('Version=2\r\n')
        for parm in ('unit', 'count', 'title', 'comment', 'timezone',
                     'time_step', 'timestamp_rounding', 'timestamp_offset',
                     'interval_type', 'variable', 'precision', 'location',
                     'altitude'):
            method_name = 'write_{}'.format(parm)
            getattr(self, method_name)(parm)

    def write_simple(self, parm):
        value = getattr(self.df, parm, None)
        if value is not None:
            self.f.write('{}={}\r\n'.format(parm.capitalize(), value))
    write_unit = write_simple
    write_title = write_simple
    write_timezone = write_simple
    write_time_step = write_simple
    write_interval_type = write_simple
    write_variable = write_simple
    write_precision = write_simple

    def write_count(self, parm):
        self.f.write('Count={}\r\n'.format(len(self.df)))

    def write_comment(self, parm):
        if getattr(self.df, 'comment', None):
            for line in self.df.comment.splitlines():
                self.f.write('Comment={}\r\n'.format(line))

    def write_timestamp_rounding(self, parm):
        timestamp_rounding_name = (self.version >= 4 and 'Timestamp_rounding'
                                   or 'Nominal_offset')
        if getattr(self.df, 'timestamp_rounding', None):
            self.f.write('{}={}\r\n'.format(timestamp_rounding_name,
                                            self.df.timestamp_rounding))

    def write_timestamp_offset(self, parm):
        timestamp_offset_name = (self.version >= 4 and 'Timestamp_offset' or
                                 'Actual_offset')
        if getattr(self.df, 'timestamp_offset', None):
            self.f.write('{}={}\r\n'.format(timestamp_offset_name,
                                            self.df.timestamp_offset))

    def write_location(self, parm):
        if self.version <= 2 or not getattr(self.df, 'location', None):
            return
        self.f.write('Location={:.6f} {:.6f} {}\r\n'.format(
            *[self.df.location[x] for x in ['abscissa', 'ordinate', 'srid']]))

    def write_altitude(self, parm):
        if (self.version <= 2) or not getattr(self.df, 'location', None) or (
                'altitude' not in self.df.location) or (
                not self.df.location['altitude']):
            return
        altitude = self.df.location['altitude']
        asrid = self.df.location['asrid'] if 'asrid' in self.df.location \
            else None
        fmt = 'Altitude={altitude:.2f} {asrid}\r\n' \
            if asrid else 'Altitude={altitude:.2f}\r\n'
        self.f.write(fmt.format(altitude=altitude, asrid=asrid))

write_file = _WriteFile()
