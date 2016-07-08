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


import csv
import os
import sys
import networkx as nx
from operator import itemgetter

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

class emptybar:
    def __init__(self):
        pass

    def update(self, i):
        pass

    def finish(self):
        pass
#end emptybar

def load_gene_sequence(genome_file, comment='#'):
    genome = []
    with open(genome_file, "r") as reader:
        for row in reader.read().replace('\r\n', '\n').splitlines():
            if not row.startswith(comment):
                genome.append(row)
    reader.close()
    return genome


def generate_map_gene_to_position(chromosome):
    return {v: k for k, v in enumerate(chromosome, start = 0)}


def read_graph_txt(graph_file, comment = '#'):
    # format: mixed list of nodes and edges
    result = nx.Graph()
    with open(graph_file, 'r') as reader:
        #for row in reader.readlines():
        for row in reader.read().replace('\r\n','\n').splitlines():
            if not row.startswith(comment):
                elem = row.split()
                if len(elem) > 1:
                    result.add_edge(elem[0], elem[1])
                elif len(elem) > 0:
                    result.add_node(elem[0])
    reader.close()
    return result


def generate_int_graph(graph, chromosome):
    # replace each node id the graph by its position in the chromosome
    # prerequise: each node in graph must exist in chromosome
    result = nx.Graph(chr=chromosome)
    result.add_nodes_from([(i,{'label': g}) for i, g in enumerate(chromosome)])
    pos = generate_map_gene_to_position(chromosome)
    missing_nodes = set()
    for s, t in graph.edges():
        try:
            result.add_edge(pos[s], pos[t])
        except KeyError:
            if s not in chromosome:
                missing_nodes.add(s)
            if t not in chromosome:
                missing_nodes.add(t)
    if missing_nodes:
        logger.warning("Following nodes are missing in the current chromosome and won't be taken in account: {}".format("\n".join(sorted(missing_nodes))))
    return result
# end


def load_graph_gexf(chromosome_list, gexf_file):
    graphs = []
    for c in chromosome_list:
        gr = nx.read_gexf(gexf_file, str, True)
        gr = generate_int_graph(gr, c)
        graphs.append(gr)
    return graphs
# end


def load_graph_txt(chromosome_list, graph_file):
    graphs = []
    for c in chromosome_list:
        gr = read_graph_txt(graph_file)
        gr = generate_int_graph(gr, c)
        graphs.append(gr)
    return graphs


# CHR_ID_FIELDNAME = 'chromosome_id'
# GENE_ID_FIELDNAME = 'gene_id'
# START_POS_ID_FIELDNAME = 'left_end_position'
# END_POS_ID_FIELDNAME = 'right_end_position'

def load_genome_tsv(input_file, chr_id_field = 'chromosome_id', gene_id_field = 'gene_id', start_pos_field = 'left_end_position', end_pos_field = 'right_end_position', comment = '#', sep = '\t'):
    result = {}
    tmp = {}
    fields = [chr_id_field, gene_id_field, start_pos_field, end_pos_field]
    with open(input_file, "r") as reader:
        lines = reader.read().replace('\r\n', '\n').splitlines()
        try:
            header_index = 0
            header = lines.pop(0)
            while header.startswith(comment):
                header = lines.pop(0)
                header_index = header_index + 1
            field_map = {s: i for i, s in enumerate(header.split(sep))}
            for f in fields:
                if f not in field_map:
                    sys.stderr.write("Field {} is missing in {}\n".format(f, input_file))
                    sys.exit(1)
            chr_id_index = field_map[chr_id_field]
            gene_id_index = field_map[gene_id_field]
            start_pos_index = field_map[start_pos_field]
            end_pos_index = field_map[end_pos_field]
            for i, l in enumerate(lines, start=header_index):
                if not l.startswith(comment):
                    values = l.split(sep)
                    try:
                        chr_id = values[chr_id_index]
                        gene_id = values[gene_id_index]
                        start_pos = int(values[start_pos_index])
                        end_pos = int(values[end_pos_index])
                        result[chr_id].append((gene_id, start_pos, end_pos))
                    except KeyError:
                        result[chr_id]=[(gene_id, start_pos, end_pos)]
                    except IndexError:
                        sys.stderr.write("Line {} in {} miss some columns\n".format(i, input_file))
                        sys.exit(1)
                    #sys.stderr.write("{}: {} \n".format(chr_id, str((gene_id, start_pos, end_pos))))
        except IndexError:
            sys.stderr.write("File {} is empty\n".format(input_file))
            sys.exit(1)
    reader.close()
    return {chr_id : [g[0] for g in sorted(gene_list, key=itemgetter(1,2))] for chr_id, gene_list in result.items()}


def numpypy_read_csv(instream, sep=';'):
    lines = instream.readlines()
    result = numpy.zeros([len(lines), len(lines)])
    for i, l in enumerate(lines, start=0):
        if not l.startswith("#"):
            for j, e in enumerate(l.split(sep), start=0):
                # print(float(e))
                result[i, j] = float(e)
    return result


def read_matrix(instream, sep =";"):
    if sys.version_info.major == 2 and sys.subversion[0] == 'CPython':
        return numpy.loadtxt(instream, delimiter=sep)
    else:
        return numpypy_read_csv(instream, sep = sep)

def numpypy_write_csv(out_stream, matrix, sep=';'):
    end = len(matrix)
    out_stream.write('\n'.join([sep.join(['%.6f' % (matrix[i,j]) for j in range(end)]) for i in range(end)]))


def export_matrix(matrix, outstream = sys.stdout):
    # numpy.savetxt() is slow with pypy or does not exist in numpy(py). It also produces the error "Mismatch between array dtype ('float64') and format specifier ('%f') with Python 3.5"
    if sys.version_info.major == 2 and sys.subversion[0] == 'CPython':
        numpy.savetxt(outstream, matrix, delimiter=';', fmt='%.6f')
    else:
        numpypy_write_csv(outstream, matrix)

def write_listing(header, listing, outstream = sys.stdout):
    if header:
        outstream.write("{}\n".format('\t'.join(header)))
    for l in listing:
        outstream.write("{}\n".format('\t'.join([str(e) for e in l])))
