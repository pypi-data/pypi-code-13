"""
utilities module for amplikyzer2
(c) 2011--2012 Sven Rahmann
"""

import os       # for filename utilities
import os.path  # for filename utilities
import glob     # for filename utilities
from configparser import ConfigParser  # for reading config files
from time import time  # for TicToc
from itertools import chain, zip_longest, islice
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor, Executor, Future
import logging
from logging.handlers import QueueHandler

from .core import ArgumentError, MissingArgumentOut


def chop(iterable, chunksize):
    """Return iterator which chops `iterable` into lists of size `chunksize`."""
    it = iter(it)
    return iter(lambda: list(islice(it, chunksize)), [])


###################################################################################################
# time utilities

class TicToc():
    """Stopwatch which gives the elapsed time as a number (method `seconds`) or
    string (method `toc`) and can be reset (method `tic`)."""

    def __init__(self):
        """Initialize instance and set start time to current time."""
        self.tic()

    def tic(self):
        """Reset to current time."""
        self.zero = time()

    def toc(self):
        """Return elapsed seconds since last reset as string (@ prepended)."""
        return "@{:.2f}".format(self.seconds())

    def seconds(self):
        """Return elapsed seconds since last reset."""
        return time() - self.zero


###################################################################################################
# string utility functions

def positionlines(numbers, digits, gapposchar="."):
    """For a given iterable `numbers` of integers and a given number of `digits`,
    return a list of `digits` strings (lines) that,
    if printed in reverse order below each other,
    constitute the vertically written `numbers` (mod 10**digits).
    """
    lines = [[] for _ in range(digits)]
    if digits <= 0:
        return lines
    for i in numbers:
        if i < 0:
            for l in lines:
                l.append(gapposchar)
        elif i == 0:
            lines[0].append("0")
            for k in range(1, digits):
                lines[k].append(" ")
        else:
            for k in range(digits):
                c = str(i % 10) if i != 0 else " "
                lines[k].append(c)
                i = i // 10
    for k in range(digits):
        lines[k] = "".join(lines[k])
    return lines

# def _test_positionlines():
#     lines = positionlines(range(7,305,7),3)
#     for rl in reversed(lines):
#         print(rl)


def adjust_str_matrix(matrix, align=">", fill=" "):
    """Adjust columns of `matrix` according to `align` using `fill` for padding.

    `matrix`: two-dimensional array of strings, which is edited in place.
    """
    assert align in "><^"
    assert len(fill) == 1
    column_widths = [
        max(map(len, column)) for column in zip_longest(fillvalue="", *matrix)]
    for row in matrix:
        row[:] = [
            '{:{}{}{}}'.format(cell, fill, align, width)
            for (cell, width) in zip(row, column_widths)]


###################################################################################################
# filename utility functions

def filenames_from_glob(path, fnames, unique=False, allowzero=True):
    """Return list of filenames from glob (`path`/`fnames`), such as '*.txt'.

    `fnames` may be a list or a string.
    If `unique == True`, ensure that there exists at most one matching file.
    If `allowzero == False`, ensure that there exists at least one file.
    In violation, a `core.ArgumentError` is raised.
    If both `unique == True` and `allowzero == False`,
      return the unique name as a string (not as 1-element list!).
    """
    if isinstance(fnames, str):
        fnames = [fnames]
    pattern = [os.path.join(path, f) if f != "-" else "-" for f in fnames]
    files = (glob.glob(p) if p != "-" else "-" for p in pattern)
    files = list(chain.from_iterable(files))

    if unique and not allowzero:
        if len(files) != 1:
            raise ArgumentError("no files or more than one file found: {}".format(pattern))
        return files[0]
    elif unique:
        if len(files) > 1:
            raise ArgumentError("more than one file found: {}".format(pattern))
    elif not allowzero and not files:
        raise ArgumentError("no files found: {}".format(pattern))
    return files


def get_outname(argout, path, filenames, extension, option="--out"):
    if argout == "-":
        return "-"
    if argout is not None:
        # not requesting stdout, so prepend path
        return os.path.join(path, argout)
    if not filenames:
        return "-"
    if len(filenames) == 1:
        base, ext = os.path.splitext(filenames[0])
        if ext == ".gz":
            base, ext = os.path.splitext(base)
        return base + extension
    raise MissingArgumentOut("must specify option '{}' for >= 2 input files".format(option))


def ensure_directory(directory):
    """Ensure that directory `directory` exists.

    It is an error to pass anything else than a directory string.
    """
    if not directory:
        return
    directory = os.path.abspath(directory)
    os.makedirs(directory, exist_ok=True)


###################################################################################################
# FASTA writing

def to_fasta(seq, linelen=60):
    i = 0
    pieces = []
    while True:
        piece = seq[i:i+linelen]
        if len(piece) == 0:
            break
        pieces.append(piece)
        i += linelen
    return "\n".join(pieces)


###################################################################################################
# config file reading

def read_config_files(path, conf):
    """Read all config files given by `args.path`, `args.conf` and return the
    `configparser.ConfigParser` object.
    """
    configfiles = filenames_from_glob(path, conf)
    parser = ConfigParser(empty_lines_in_values=False, interpolation=None)
    parser.optionxform = str  # allow case-sensitive keys
    parser.read(configfiles, encoding="utf-8")
    return parser


def labels_from_config(configinfo):
    """Parse labels from `configinfo` object.
    MID, LOCUS = Patient Name
    """
    labels = dict()
    if "LABELS" not in configinfo:
        return labels  # empty dictionary if no labels present
    for key, value in configinfo.items("LABELS"):
        # key must be "MID, LOCUS" or "MID" alone
        # the presence of the comma distinguishes both cases
        if "," in key:  # "MID, LOCUS"
            mid, locus = key.split(",")
            key = (mid.strip(), locus.strip())
        labels[key] = value
    return labels


def get_label(labels, mid, locus=None):
    """Return label from `dict` `labels` for `(mid, locus)`.

    If there is no label for `(mid, locus)` return label for `mid`.
    If there is no label for `mid` either simply return `mid` itself."""
    key = (mid, locus)  # never exists when locus is None
    if key in labels:
        return labels[key]
    return labels.get(mid, mid)


###################################################################################################
# multiprocessing utilities

class SerialExecutor(Executor):
    def __init__(self, max_workers=None):
        if max_workers is not None and max_workers != 1:
            raise ValueError("number of workers must be exactly one")
        self._shutdown = False

    def map(self, func, *iterables, timeout=None, chunksize=1):
        if self._shutdown:
            raise RuntimeError("cannot schedule new futures after shutdown")
        # NOTE: This simplification differs from behavior in Executor.map, since
        #       Executor.map consumes *iterables before dispatch!
        return map(func, *iterables)

    def submit(self, fn, *args, **kwargs):
        if self._shutdown:
            raise RuntimeError("cannot schedule new futures after shutdown")
        future = Future()
        try:
            result = fn(*args, **kwargs)
        except BaseException as e:
            future.set_exception(e)
        else:
            future.set_result(result)
        return future

    def shutdown(self, wait=True):
        self._shutdown = True


def get_executor(max_workers, serial=False):
    """Return either a `concurrent.futures.ProcessPoolExecutor` or a `SerialExecutor`.

    Only return `SerialExecutor` if `serial` is `True` or `max_workers` is `None`.
    If `max_workers` is 0 `multiprocessing.cpu_count()` is used instead.
    """
    if serial or max_workers is None:
        return SerialExecutor()
    if max_workers == 0:
        max_workers = cpu_count()
    return ProcessPoolExecutor(max_workers)


def executor_map(executor, fn, *iterables, timeout=None, queuesize=None):
    """Return an iterator equivalent to `map(fn, *iterables)`.

    !!Copy of `concurrent.futures.Executor.map` which does not consume
    `iterables` all at once but uses an internal queue of size `queuesize`!!

    Args:
        fn: A callable that will take as many arguments as there are
            passed iterables.
        timeout: The maximum number of seconds to wait. If None, then there
            is no limit on the wait time.
        queuesize: Maximum size of queue. If None, then Executor.map is
            called directly.

    Returns:
        An iterator equivalent to: map(func, *iterables) but the calls may
        be evaluated out-of-order.

    Raises:
        TimeoutError: If the entire result iterator could not be generated
            before the given timeout.
        Exception: If fn(*args) raises for any values.
    """
    if queuesize is None:
        return executor.map(fn, *iterables, timeout=timeout)

    if timeout is not None:
        end_time = timeout + time.time()

    # The following replaces the original code
    # `fs = [self.submit(fn, *args) for args in zip(*iterables)]`
    # from `concurrent.futures.Executor.map` by `queued_futures`
    iterables = zip(*iterables)
    queue = []

    def queued_futures():
        while True:
            while len(queue) < queuesize:
                try:
                    args = next(iterables)
                except StopIteration:
                    break
                queue.append(executor.submit(fn, *args))
            if not queue:
                return
            yield queue.pop(0)

    # Yield must be hidden in closure so that the futures are submitted
    # before the first iterator value is required.
    def result_iterator():
        try:
            for future in queued_futures():
                if timeout is None:
                    yield future.result()
                else:
                    yield future.result(end_time - time.time())
        finally:
            for future in queue:
                future.cancel()
    return result_iterator()


def verbose_pool_map(map_func, func, iterable, *args, **kwargs):
    """Apply `func` to `iterable` through `map_func`; re-raise exceptions which
    are raised by `iterable`.

    `multiprocessing.Pool.imap` may not pass through an exception from
    generator `iterable` to caller, so this function saves and re-raises it.
    Example usage:
        def generator(n, x):
            for i in range(n):
                if i == x:
                    raise RuntimeError
                yield i
        def func(i):
            return 2 * i
        with multiprocessing.Pool(2) as pool:
            n, x, c = 10, 2, 4
            assert x < c <= n
            sum(pool.imap(func, generator(n, x), chunksize=c))
            # no RuntimeError raised
            sum(verbose_pool_map(pool.imap, func, generator(n, x), chunksize=c))
            # RuntimeError raised through verbose_pool_map
    """
    caught_exception = []

    def exception_catcher():
        try:
            yield from iterable
        except Exception as e:
            caught_exception[:] = [e]
            raise
    yield from map_func(func, exception_catcher(), *args, **kwargs)
    if caught_exception:
        raise caught_exception[0]


class LogRecordDelegator:
    """`logging.Handler`-like class for `logging.handlers.QueueListener`.

    Forwards all `logging.LogRecord` instances to their appropriate loggers.
    """
    def handle(self, record):
        logging.getLogger(record.name).handle(record)


def init_queue_logging(log_queue, level=logging.INFO):
    """Remove all logging handlers and register a `logging.handlers.QueueHandler`
    for `log_queue` on the root logger.

    Must not be called in main process but only in subprocesses during their
    initialization.
    """
    root_logger = logging.getLogger()
    loggers = chain([root_logger], logging.Logger.manager.loggerDict.values())
    for logger in loggers:
        if isinstance(logger, logging.PlaceHolder):
            continue
        for handler in logger.handlers.copy():
            logger.removeHandler(handler)
    root_logger.addHandler(QueueHandler(log_queue))
    root_logger.setLevel(level)
