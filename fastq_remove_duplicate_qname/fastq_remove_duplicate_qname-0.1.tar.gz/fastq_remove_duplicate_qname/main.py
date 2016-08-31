#!/usr/bin/env python

import argparse
import logging
import sys

from Bio import SeqIO

def main():
    parser = argparse.ArgumentParser('remove duplicate reads from fastq')
    parser.add_argument('infile',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin
    )
    parser.add_argument('outfile',
                        nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout
    )
    parser.add_argument('-l', '--log_file_path',
                        required = True,
                        help = 'log file path'
    )
    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile
    log_file_path = args.log_file_path
    
    logging.basicConfig(
        filename=log_file_path,
        filemode='a',
        level = logging.INFO,
        #format='%(asctime)s %(levelname)s %(message)s',
        #datefmt='%Y-%m-%d_%H:%M:%S_%Z',
    )
    logger = logging.getLogger(__name__)

    singleton_set = set()
    readcounter = 0
    duplicatecounter = 0
    for record in SeqIO.parse(infile,'fastq'):
        if record.id in singleton_set:
            duplicatecounter += 1
            logger.info('duplicate:\t%s' % record.id)
        else:
            readcounter += 1
            singleton_set.add(record.id)
            SeqIO.write(record, outfile, 'fastq')
    logger.info('readcounter:\t%s' % str(readcounter))
    logger.info('duplicatecounter:\t%s' % str(duplicatecounter))
    return

if __name__ == '__main__':
    main()
