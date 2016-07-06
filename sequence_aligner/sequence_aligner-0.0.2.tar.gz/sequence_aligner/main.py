#!/usr/bin/python
# coding= utf8

from argparse import ArgumentParser
from datetime import datetime

from fasta_parser import FastaParser
from sequence_aligner import SequenceAligner
from tools import make_storage_path, write_results_to_file


def options():
    """
    Command line arguments for running and customizing program
    :return: parsed arguments
    """
    parser = ArgumentParser(description="DNA Sequence Alignment")
    parser.add_argument('--file_path',
                        type=str,
                        help='the exact path to file'
                             ' with FASTA sequences',
                        required=True)
    parser.add_argument('--storage_path',
                        type=str,
                        help='directory where results'
                             ' are to be stored',
                        default='/tmp/sequence_results',
                        required=False)
    parser.add_argument('--results_name',
                        type=str,
                        help='file name - no spaces.'
                             'will store as txt file.',
                        default="sequence_read-{}.txt".format(
                            datetime.now(). isoformat().replace(":", "."),
                            required=False))
    return parser.parse_args()


def main():
    opt = options()
    fp = FastaParser(opt.file_path)
    sequence_list = fp.get_sequence_list()
    print "#" * 10
    print "#" * 10
    ss = datetime.now()
    print "Starting..."
    sa = SequenceAligner(sequence_list)
    results = sa.get_aligned_sequence()
    print "Process complete. Results on the way...."
    storage_path = make_storage_path(opt.storage_path)
    results_path = write_results_to_file(
        results, opt.results_name, storage_path)
    elapsed = datetime.now() - ss
    print "Job completed after {} min".format(elapsed.total_seconds()/60)
    print "Sequence Alignment results stored --> {}".format(results_path)
    print "#" * 10
    print "#" * 10

if __name__ == "__main__":
    main()
