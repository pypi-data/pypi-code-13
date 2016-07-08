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
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

## import local submodules
try:
    import libs
    import DCC_matrix as dcc_connected
    import DCC_domination as dom
    import DCC_listing
    from gbk import load_gbk
except ImportError:
    import gtsegments.libs as libs
    import gtsegments.DCC_matrix as dcc_connected
    import gtsegments.DCC_domination as dom
    import gtsegments.DCC_listing as DCC_listing
    from gtsegments.gbk import load_gbk


MAX_LENGTH_WARNING = 100

################
# Main program #
################
def main (argv, prog = os.path.basename(sys.argv[0])):
    import argparse
    import textwrap
    logger = logging.getLogger(__package__)
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.INFO)

    #logger.setFormatter(formatter)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Compute the list of GTsegments from a genome and a coexpression network.

        example:
        %(prog)s -min 2 -max 50 -d 0.6 coexp_graph.gexf genome.gbk
        '''),
        prog = prog
    )

    #######################
    # Requiered arguments #
    #######################

    parser.add_argument(
        'coexp_graph', help='Coexpression graph', metavar='COEXP_GRAPH')

    parser.add_argument(
        'genome', nargs='*', help='genome file(s) containing genomic organization of chromosomes', metavar='GENOME')

    ######################
    # Optional arguments #
    ######################


    typep = parser.add_argument_group(title='File type')

    typep.add_argument('--genome_type',
                        default='gbk', choices=['gbk', 'tsv', 'seq'],
                        help='Type of the genome file(s) (default: %(default)s)')

    typep.add_argument('--graph_type',
                        default='gexf', choices=['gexf', 'list'],
                        help='Type of the coexpression graph file (default: %(default)s)')

    # Segment size
    ##############

    segp = parser.add_argument_group(title='GTsegments size')

    segp.add_argument('-min', '--min_size', metavar='INT',
                      type=int, default=2,
                      help='Minimum length of a GTsegment (default: %(default)s)')

    segp.add_argument('-max', '--max_size', metavar='INT',
                      type=int, default=sys.maxsize,
                      help='Maximum length of a GTsegment (default: maximum possible)')

    # segp.add_argument('-all', '--all_gtsegments',
    #                   default=False, action='store_true',
    #                   help='Ignore the genomic segment size limits')


    # Density threshold
    ###################

    densityp = parser.add_argument_group(title='Density option')

    densityp.add_argument('-d', '--density', metavar='THRESHOLD',
                          type=float, default=0.6,
                          help='Select GTsegments with a genomic density ≥ %(metavar)s in ]0,1] (default: %(default)s)')

    densityp.add_argument('--no_filter',
                          default=False, action='store_true',
                          help='Do not apply density filtering')


    # Outputs options
    #################

    outp = parser.add_argument_group(title='Output options')

    outp.add_argument('-o', '--output', metavar='FILE',
                      help='Output file name')

    outp.add_argument('-no_dom', '--no_domination',
                      default=False, action='store_true',
                      help='Keep all the GTsegments instead of the dominant ones')

    outg = outp.add_mutually_exclusive_group()

    outg.add_argument('-m', '--matrix',
                      default=False, action='store_true',
                      help='Output the density matrix instead of the listing of GTsegments')

    outg.add_argument('--no_gene_list',
                      default=False, action='store_true',
                      help='Do not add the gene list column in the listing of GTsegments')


    # Messages
    ##########
#    parser.add_argument('-log', '--log_file', metavar='LOG_FILE',
#                        help='All log messages will be stored in the given file')

    verbose_group = parser.add_mutually_exclusive_group()
#    verbose_group.add_argument('-v', '--verbose', action='store_true',
#                               help='Verbose mode: display all messages.')
    verbose_group.add_argument('-q', '--quiet',  action='store_true',
                               help='Quiet mode: display only critical errors')
    #verbose_group.add_argument('-debug', '--debug', action='store_true',
    #                           help='Debug mode: diplay all messages')

    args = parser.parse_args()

    ################
    # Logging part #
    ################

    # if args.debug:
    #    # Set logging level to debug
    #    logger.setLevel(logging.DEBUG)
    if args.quiet:
        # Set logging level to quiet
        logger.setLevel(logging.CRITICAL)
    #if args.verbose:
        # Set logging level to verbose
    #    logger.setLevel(logging.INFO)

    # Add log file
    # if args.log_file:
    #     log_file = logging.FileHandler(args.log_file)
    #     log_file.setLevel(logging.INFO)
    #     logger.addHandler(log_file)

    ####################
    # Load input files #
    ####################

    chromosome_id_list = args.genome

    if args.genome_type == 'gbk':
        logger.info('Loading genome from gbk files')
        chromosome_list = []
        chromosome_id_list = []
        for f in args.genome:
            #sys.stderr.write("{}\n".format(str(load_gbk(f).items())))
            for chr_id, gene_list in load_gbk(f).items():
                chromosome_list.append(gene_list)
                chromosome_id_list.append(chr_id)
        sys.exit(0)

    elif args.genome_type == 'tsv':
        logger.info('Loading genome from tsv files')
        chromosome_list = []
        chromosome_id_list = []
        for f in args.genome:
            #sys.stderr.write("{}\n".format(str(load_gbk(f).items())))
            for chr_id, gene_list in libs.load_genome_tsv(f).items():
                chromosome_list.append(gene_list)
                chromosome_id_list.append(chr_id)

    else: # args.genome_type == 'seq'
        logger.info('Loading genome from circular unichromosomal sequence files')
        chromosome_list = [libs.load_gene_sequence(chromosome) for chromosome in args.genome]

    if args.graph_type == 'gexf':
        logger.info('Loading graph from gefx file')
        graphs = libs.load_graph_gexf(chromosome_list, args.coexp_graph)
    else: # list
        logger.info('Loading graph from list file (.txt)')
        graphs = libs.load_graph_txt(chromosome_list, args.coexp_graph)

    ###################################
    # Check and correct option values #
    ###################################

    # Density
    d = max(0.0, min(args.density, 1.0))
    if d != args.density:
        logger.warning(
            'Genomic density threshold ({}) is not in ]0,1]. Using {} instead.'.format(args.density, d))


    ######################
    # Do the computation #
    ######################
    if args.output:
        try:
            outstream = file(args.output, 'w')
        except :
            logger.error('Cannot open {} file'.format(args.output))
            exit(1)
    else:
        outstream = sys.stdout

    for i, gr in enumerate(graphs, start=0):
        chromosome = chromosome_list[i]
        chromosome_id = chromosome_id_list[i]
        genes_number = len(gr.nodes())
        logger.info('Working on {} chromosome.'.format(chromosome_id))

        # Check segment sizes
        min_window_size = max(1, min(args.min_size, genes_number))
        if min_window_size != args.min_size:
            logger.warning('Minimum GTsegment size ({}) is not in [1,{}]. Using {} instead.'.format(
                args.min_size, genes_number, min_window_size))
        max_window_size = max(1, min(args.max_size, genes_number))
        if max_window_size != args.max_size and args.max_size != sys.maxsize:
            logger.warning('Maximum GTsegment size ({}) is not in [1,{}]. Using {} instead.'.format(
                args.max_size, genes_number, max_window_size))
        if not args.no_gene_list and max_window_size >= MAX_LENGTH_WARNING:
            logger.warning(
                'Important maximum segment size (-max ≥ {}) can produce a huge result file. Please consider the --no_gene_list option, in particular when using the --no_domination option.'.format(MAX_LENGTH_WARNING))


        logger.info('Compute density matrix with [{},{}] segment size'.format(min_window_size, max_window_size))
        density_matrix = dcc_connected.dcc_matrix_compute(gr, min_window_size, max_window_size)

        if not args.no_filter:
            logger.info('Filtering density matrix by keeping value ≥ {}.'.format(d))
            density_matrix[density_matrix < d] = 0

        if not args.no_domination:
            logger.info('Compute domination')
            density_matrix = dom.compute(density_matrix, min_window_size, max_window_size)

        if args.matrix:
            libs.export_matrix(density_matrix, outstream)
        else:
            logger.info('Convert density matrix to listing of GTsegments')
            header, listing = DCC_listing.convert(density_matrix, gr, chromosome, min_window_size, max_window_size, gene_listing = not args.no_gene_list)

            logger.info('Export listing of GTsegments to tsv file')
            # add chromosome id to listing
            header.insert(0, 'chromosome')
            for l in listing:
                l.insert(0, chromosome_id)
            libs.write_listing(header, listing, outstream)

    if args.output:
        outstream.close()
    # end

if __name__ == '__main__':
    main(sys.argv[1:])
