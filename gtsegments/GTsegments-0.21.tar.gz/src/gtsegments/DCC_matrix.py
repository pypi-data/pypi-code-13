#!/usr/bin/env python
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


# An interval of genes [a..b] from the genome is an unique id that can be used to identify a connected subgraph into the coexpression network. The connected subgraph is induced by the connected component that contains a and b into the subgraph induced by the set of genes into [a..b].
# It is possible to compute the genomic density of this connected subgraph (i.e. the number of genes of the interval that appears into the subgraph)
# This program compute then the martix of density of the whole possible intervals
# 1) for each gene of the genome, we processed this way:
# 2) the gene alone is into the first connected component. It density is 1
# 3) until the a sequence loop is done
# 4) extend the interval by adding the next gene (alway by the same side)
# 5) get the neighborhood of the new gene (O(deg)) and put the new gene into the right connected component (O(1)). Make the union of the contected component that the new gene connects allows that (O(deg)): at worst, each neighbor is in a different component).
# 6) by maintainning the number of genes in each connected component, I think it is possible to compute density in O(1).
# 7) end

# The complexity of this algorithm is near O(m.n^2) with m the number of arcs and n the number of vertices (genes).
# Creating the listing of gene into a components from an interval id can be done with a deep/breadth first like algorithm.
# It is also possible to used the step 5 to create a graph/matrix of
# included, tangled and overlapping intervals (need more reflexion)

from __future__ import division

import os
import sys

import networkx as nx
import ufx.uf_hash as ufx
try:
    from libs import *
except ImportError:
    from gtsegments.libs import *


#import multiprocessing
import progressbar
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__package__)

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


def update_uf(uf, start, end, gr):
    # add current end to the independent set structure
    end_id = uf.make_set(end)
    # put neigbors of the current end of the segment in same component if they are in the segment
    if start <= end:
        for n in gr.neighbors(end):
            if start <= n <= end:
                end_id = uf.union(end_id, n)
    else:
        for n in gr.neighbors(end):
            if n <= end or start <= n:
                end_id = uf.union(end_id, n)
    return end_id


def dcc_submatrix_update(gr, density_matrix, min_window_size, max_window_size, start, end):
    #sys.stderr.write("Filling density matrix\n")
    size=len(gr.nodes())
    if logger.isEnabledFor(logging.INFO):
        bar = progressbar.ProgressBar(max_value=end-start).start()
    else:
        bar = emptybar()
    for i in range(start, end):
        uf = ufx.UnionFind()
        uf.make_set(i)
        density_matrix[i,i] = 1.0 # the genomic density of an interval of one gene is 1

        # reach the min_window_size with correct independant sets
        for segment_size in range(2, min_window_size):
            j = (i + segment_size - 1) % size
            set_id = update_uf(uf, i, j, gr)

        # fill the density matrix now
        for segment_size in range(min_window_size, max_window_size + 1):
            j = (i + segment_size - 1) % size
            set_id = update_uf(uf, i, j, gr)

            # segment is valid if the current ending and the begining of the segment are in the same component
            if uf.find(i) == set_id:
                density_matrix[i,j] = uf.get_size(set_id) / float(segment_size)
                #sys.stderr.write("{}:{}\n".format(str((i,j)), density_matrix[i,j]))
        #end while
        uf.clear()
        bar.update(i - start)
    bar.finish()
#end

def dcc_submatrix_update_cc(gr, density_matrix, min_window_size, max_window_size, start, end, next_connected):
    #sys.stderr.write("Filling density matrix\n")
    size=len(gr.nodes())
    if logger.isEnabledFor(logging.INFO):
        bar = progressbar.ProgressBar(max_value=end-start).start()
    else:
        bar = emptybar()
    for i in range(start, end):
        uf = ufx.UnionFind()
        set_id = uf.make_set(i)
        density_matrix[i,i] = 1.0 # the genomic density of an interval of one gene is 1

        # fill the ufx structure to reach the window size
        j, dist = next_connected[i]
        segment_size = dist + 1
        while segment_size < min_window_size and j != i:
            set_id = update_uf(uf, i, j, gr)
            j, dist = next_connected[j] # next gene
            segment_size = segment_size + dist # the length of the sequence is increased
        # fill the density matrix now
        while segment_size <= max_window_size and j != i:
            set_id = update_uf(uf, i, j, gr)
            if uf.find(i) == set_id:
                density_matrix[i,j] = uf.get_size(set_id) / float(segment_size)
                #sys.stderr.write("{}:{}\n".format(str((i,j)), density_matrix[i,j]))
            j, dist = next_connected[j] # next gene
            segment_size = segment_size + dist # the length of the sequence is increased
        #end while
        uf.clear()
        bar.update(i - start)
    bar.finish()

def dcc_matrix_compute(gr, min_window_size, max_window_size):
    size = len(gr.nodes())
    density_matrix = numpy.zeros([size,size]) # size * size matrix filled with 0.0

    cc = [sorted(c) for c in nx.connected_components(gr)]
    next_right_connected = {}
    for i, c in enumerate(cc):
        # next_right_connected associates to each node 1) the nearest right node in right side of the segment that is in the same cc and 2) the distance that separate them.
        next_right_connected.update({c[j]: (c[(j+1)%len(c)], (c[(j+1)%len(c)] - c[j])% size) for j in range(len(c))})

    #dcc_submatrix_update(gr, density_matrix, min_window_size, max_window_size, 0, size)
    dcc_submatrix_update_cc(gr, density_matrix, min_window_size, max_window_size, 0, size, next_right_connected)

    return density_matrix


################
# Main program #
################
def main (argv, prog = os.path.basename(sys.argv[0])):
    import argparse
    import textwrap
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Compute then density matrix given a genome and a coexpression graph

        exemple:
        python %(prog)s -min 2 -max 50 graph.txt chromosome.txt
        '''),
        prog = prog
    )

    # Requiered arguments
    #####################
    genp = parser.add_argument_group(title="Data")
    genp.add_argument(
        "coexp_graph", help="Coexpression graph")
    genp.add_argument(
        "gene_seq", help="gene sequence file representing the circular unichromosomal genome")

    # Optional arguments
    ####################
    seqp = parser.add_argument_group(title="optional sequence constraints")
    seqp.add_argument("-min", "--min_seq_size", type=int,
                      default=1, help="minimum size of the sequence")
    seqp.add_argument("-max", "--max_seq_size", type=int,
                      default=sys.maxsize, help="maximum size of the sequence")

    # Messages
    ##########
    parser.add_argument('-log', '--log_file', metavar='LOG_FILE',
                        help='All log messages will be stored in the given file')

    verbose_group = parser.add_mutually_exclusive_group()
    verbose_group.add_argument('-v', '--verbose', action='store_true',
                               help='Verbose mode: display all messages.')
    verbose_group.add_argument('-q', '--quiet',  action='store_true',
                               help='Quiet mode: diplay only critical errors')
    sys.stderr.write("Loading graph\n")

    args = parser.parse_args()

    chromosome = load_gene_sequence(args.gene_seq)
    gr = load_graph_txt([chromosome], args.coexp_graph)[0]

    chr_size = len(chromosome)

    sys.stderr.write("Compute density matrix\n")
    density_matrix = dcc_matrix_compute(gr, min(args.min_seq_size, chr_size), min(args.max_seq_size, chr_size))
    sys.stderr.write("\nExport matrix\n")
    # numpy.savetxt() is slow with pypy or does not exist in numpypy. It also produces the error "Mismatch between array dtype ('float64') and format specifier ('%f') with Python 3.5"
    export_matrix(density_matrix, sys.stdout)

    # end

if __name__ == '__main__':
    main(sys.argv[1:])
