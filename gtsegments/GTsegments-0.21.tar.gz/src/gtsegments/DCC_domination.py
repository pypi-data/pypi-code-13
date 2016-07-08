# -*- encoding: utf-8 -*-
# Copyright (c) 2013-2016, Philippe Bordron <philippe.bordron+GTsegments@gmail.com>
#
# This file is part of GTsegments.
#
# GTsegments is free software: you can redistribute it and/or modify
# it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GTsegments is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
# along with GTsegments.  If not, see <http://www.gnu.org/licenses/>


# Compute domination over DDC matrix.

import os
import sys
import progressbar

import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__package__)

try:
    from libs import emptybar
except ImportError:
    from gtsegments.libs import emptybar

try:
    import numpy
except ImportError:
    try:
        import numpypy as numpy
    except ImportError:
        try:
            import _numpypy as numpy
        except ImportError:
            logger.critical("Please install numpy!")
            exit(1)


def compute(matrix, min_window_size, max_window_size):

    # there is a relationship between row and columns
    rows = {}  # get row of a given column
    columns = {}  # get column of a given row
    size = matrix.shape[0]
    dominated_by = numpy.empty([size, size, 2], dtype=int)

    # each entry (x,y) point to the couple (x',y')
    # such as (x',y) and (x,y') dominates (x,y)
    # x' can be equal to x and y' can be equal to y
    # in this case it can exist no domination

    if logger.isEnabledFor(logging.INFO):
        bar = progressbar.ProgressBar(max_value=max_window_size - min_window_size + 1).start()
    else:
        bar = emptybar()
    for offset in range(max_window_size - 1, min_window_size - 2, -1):
        for i in range(size):
            j = (i + offset) % size
            d = matrix[i, j]
            # find no included dcc
            if d > 0:
                if not i in columns:
                    columns[i] = j
                    if not j in rows:
                        rows[j] = i
                        dominated_by[i, j] = [i, j]
                    else:
                        dominated_by[i, j] = [rows[j], j]
                        # columns[i]=j
                        # rows[j]=i
                    # print "%d : columns[%d] -> %d vs %d" % (offset, i,
                    # columns[i], j)
                elif not j in rows:
                    dominated_by[i, j] = [i, columns[i]]
                    #columns[i]=j
                    rows[j] = i
                    #print "%d : rows[%d] -> %d vs %d" % (offset, j,rows[j], i)
                # find domination
                r = rows[j]
                c = columns[i]
                # update rows
                x1, y1 = dominated_by[r, j]
                x2, y2 = dominated_by[i, c]
                # update domination relationship
                if d > matrix[x1, y1] and d > matrix[x2, y2]:
                    # itself domination
                    dominated_by[i, j] = [i, j]
                else:
                    if matrix[x1, y1] < d <= matrix[x2, y2]:
                        # dominated by a (larger) segment with the same end (column)
                        dominated_by[i, j] = [x2, y2]
                    if matrix[x2, y2] < d <= matrix[x1, y1]:
                        # dominated by a (larger) segment with the same start (row)
                        dominated_by[i, j] = [x1, y1]
                    if d <= matrix[x1, y1] and d <= matrix[x2, y2]:
                        if matrix[x1, y1] > matrix[x2, y2]:
                            dominated_by[i, j] = [x1, y1]
                        else:
                            dominated_by[i, j] = [x2, y2]
                    if dominated_by[i, j, 0] != i or dominated_by[i, j, 1] != j:
                        matrix[i, j] = 0.0  # remplace dominated density by 0
                rows[j] = i
                columns[i] = j
        bar.update(max_window_size - offset)
    bar.finish()
    # print ""
    # print matrix
    # print dominated_by
    columns.clear()
    rows.clear()
    return matrix
# end

################
# Main program #
################
if __name__ == '__main__':
    import argparse
    import textwrap
    try:
        from libs import *
    except ImportError:
        from dcc.libs import *
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Remove the dominated DCC from the density matrix

        exemple:
        python %(prog)s -max 50 < density_matrix.csv
        ''')
    )

    # Optional arguments
    ####################
    seqp = parser.add_argument_group(title="optional sequence constraints")
    seqp.add_argument("-min", "--min_seq_size", type=int,
                      default=2, help="minimum size of the sequence")
    seqp.add_argument("-max", "--max_seq_size", type=int,
                      default=sys.maxint, help="maximum size of the sequence")

    #verbose_group = parser.add_mutually_exclusive_group()
    #verbose_group.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
    #verbose_group.add_argument("-q", "--quiet", help="quiet mode", action="store_true")
    parser.add_argument("-q", "--quiet", help="quiet mode",
                        action="store_true")

    args = parser.parse_args()

    if args.quiet:
        sys.stderr.write('quiet option not implemented now\n')

    sys.stderr.write("Load density matrix\n")
    matrix = read_matrix(sys.stdin)
    size = len(matrix)
    sys.stderr.write("%d x %d matrix\n" % (size, size))

    sys.stderr.write("Compute domination\n")
    matrix = compute(matrix, min(max(2,
        args.min_seq_size), size), min(args.max_seq_size, size))
    sys.stderr.write("\nExport matrix\n")
    export_matrix(matrix)
# end
