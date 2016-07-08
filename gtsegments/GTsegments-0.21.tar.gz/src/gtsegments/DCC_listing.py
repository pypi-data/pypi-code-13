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


import os
import sys
import networkx as nx
from operator import itemgetter
import itertools as it
#from llist import dllist, dllistnode
import progressbar
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__package__)

try:
    from libs import *
except ImportError:
    from gtsegments.libs import *

def get_active_genes_index(gr, chromosome, start_pos, end_pos):
    # gr : coexpression graph,
    # chromosome: gene sequence,
    # start_pos & end_pos : start and end position of the interval
    # first get the subset of genes that are allowed into the graph
    if (start_pos <= end_pos):
        subgraph_nodes = range(start_pos, end_pos + 1)
    else:
        subgraph_nodes = it.chain(range(start_pos, len(chromosome)), range(0, end_pos + 1))
    # endif
    # then do a traversal with a cutting when the next vertice is not allowed
    subgraph = gr.subgraph(subgraph_nodes)
    return nx.node_connected_component(subgraph, start_pos)
# end def

# To remove
def allowed_reachability(gr, subgraph_nodes, start):
    nodes = set(subgraph_nodes)
    result = set()
    pile = list()
    pile.append(start)
    #sys.stderr.write("{}\n".format("\n".join([str(n) + ":" + gr.node[n]['label'] for n in gr.nodes()])))
    while pile:
        n = pile.pop()
        #sys.stderr.write("{}\n".format(n))
        result.add(n)
        neighbors = gr.neighbors(n)
        for v in neighbors:
            if v in subgraph_nodes and (not v in result):
                pile.append(v)
    return result
# end def

def follow_the_strand(gene_list, chromosome, start_pos, end_pos):
    if (start_pos <= end_pos):
        return sorted(gene_list)
    else:
        result = []
        # TODO: find a way to used sorting key with circular list...
        for x in range(start_pos,len(chromosome)):
            if x in gene_list:
                result.append(x)
        for x in range(0, end_pos + 1):
            if x in gene_list:
                result.append(x)
        return result
# end def

def convert(matrix, gr, chromosome, min_window_size, max_window_size, gene_listing=True):
    header = ["start", "end", "length", "active_genes", "density"]
    if gene_listing:
        header.append("list_of_active_genes")
    listing = []
    size = matrix.shape[0]
    #sys.stderr.write('{} density matrix\n'.format(matrix.shape))
    if logger.isEnabledFor(logging.INFO):
        bar = progressbar.ProgressBar(max_value=size).start()
    else:
        bar = emptybar()
    for r in range(0, size):
        for offset in range(min_window_size, max_window_size + 1):
            c = (r + offset - 1) % size
            # when the density is <=0, it's not an valid interval, then it is
            # not needed to produce the corresponding interval
            d = float(matrix[r][c])
            if d > 0:
                if gene_listing:
                    active_genes_index = get_active_genes_index(gr, chromosome, r, c)
                    # print gene_set
                    active_genes = [gr.node[n]['label'] for n in  follow_the_strand(set(active_genes_index), chromosome, r, c)]
                    # do a deep first search and cut each branch each time the node
                    # is outside of the interval
                    listing.append([r + 1, c + 1, offset, int(round(offset * d)), d, ' '.join(active_genes)])
                else:
                    listing.append([r + 1, c + 1, offset, int(round(offset * d)), d])
        bar.update(r)
    # end
    bar.finish()
    listing.sort(key=itemgetter(0,1))
    return header, listing

################
# Main program #
################
def main (argv, prog = os.path.basename(sys.argv[0])):
    import argparse
    import textwrap
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Transform a density matrix into a listing

        exemple:
        python %(prog)s -min 2 -max 50 graph.txt chromosome.txt < density_matrix.txt
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

    #verbose_group = parser.add_mutually_exclusive_group()
    #verbose_group.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
    #verbose_group.add_argument("-q", "--quiet", help="quiet mode", action="store_true")
    parser.add_argument("-q", "--quiet", help="quiet mode",
                        action="store_true")

    # Developper options
    args = parser.parse_args()

    if args.quiet:
        sys.stderr.write('quiet option not implemented now\n')

    sys.stderr.write("Loading chromosome\n")
    chromosome = load_gene_sequence(args.gene_seq)
    chromosome_size = len(chromosome)

    sys.stderr.write("Loading graph\n")
    gr = load_graph_txt([chromosome], args.coexp_graph)[0]
    #sys.stderr.write("{}\n".format("\n".join([str(n) + ":" + gr.node[n]['label'] for n in gr.nodes()])))

    min_window_size = max(0, min(args.min_seq_size, chromosome_size - 1))
    max_window_size = max(0, min(args.max_seq_size, chromosome_size - 1))

    # read the matrix from stdin
    sys.stderr.write('Read matrix from stdin\n')
    matrix = read_matrix(sys.stdin)
    sys.stderr.write('Convert matrix to listing\n')
    header, listing = convert(matrix, gr, chromosome, min_window_size, max_window_size)
    # sort listing by position

    sys.stderr.write('Write listing\n')
    write_listing(header, listing, sys.stdout)

if __name__ == '__main__':
	main(sys.argv[1:])
