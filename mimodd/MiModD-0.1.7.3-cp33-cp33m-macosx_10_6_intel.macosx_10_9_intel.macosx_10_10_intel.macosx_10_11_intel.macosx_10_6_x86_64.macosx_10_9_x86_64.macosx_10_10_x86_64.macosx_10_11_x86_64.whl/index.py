import os
from . import pysamtools

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(usage = argparse.SUPPRESS,
                                     formatter_class = argparse.RawDescriptionHelpFormatter,
                                     description = """

generate an index file for a supported sequence file type
(well, currently BAM is the only supported type).

""")
    parser.add_argument('ifile', metavar = 'FILE_TO_INDEX')
    args = vars(parser.parse_args())

    inputfile = os.path.realpath(os.path.expanduser(args['ifile']))
    if not os.path.isfile(inputfile):
        raise FileNotFoundError('File to index does not seem to exist: {0}'.format(inputfile))
    print ()
    print ('running samtools index on', inputfile, '...')
    run_info = pysamtools.index(inputfile, reindex = True)
    print ('command: "{0}" finished.'.format(run_info.call))
    print ()
    assert os.path.isfile(inputfile + '.bai'), 'Something unexpected happened. Could not generate index file.'
    print ('index file is at: {0}.bai'.format(inputfile))
