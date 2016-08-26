#!/usr/bin/env python

import argparse
import logging
import os
import subprocess
import sys

def setup_logging(args, ban_name):
    logging.basicConfig(
        filename=os.path.join(bam_name + '.log'),
        level=args.level,
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d_%H:%M:%S_%Z',
    )
    logger = logging.getLogger(__name__)
    return logger

def get_bam_header(bam_path):
    bam_name = os.path.basename(bam_path)
    header_name = bam_name + '.header'

    samtools_path = os.path.join('/usr', 'local', 'bin', 'samtools')
    cmd = [samtools_path, 'view', '-H', bam_path, '>', header_name]
    shell_cmd = ' '.join(cmd)
    output = subprocess.check_output(shell_cmd, shell=True)
    return header_name
    
def reheader_bam(bam_path, logger):
    step_dir = os.getcwd()
    bam_name = os.path.basename(bam_path)

    #orig header path
    orig_bam_header = get_bam_header(bam_path)

    #new header path
    reheader = bam_name + '.reheader'
    cmd = ['head', '-n1', orig_bam_header, '>', reheader]
    shell_cmd = ' '.join(cmd)
    output = subprocess.check_output(shell_cmd, shell=True)

    #remove @SQ from orig header
    cmd = ["sed", "-i", "'/^@SQ/d'", orig_bam_header]
    shell_cmd = ' '.join(cmd)
    output = subprocess.check_output(shell_cmd, shell=True)

    #new @SQ
    python_version = str(sys.version_info.major) + '.' + str(sys.version_info.minor)
    gdc_sq_header_path = os.path.join('/usr', 'local', 'lib', 'python'+python_version, 'dist-packages',
                                      'bam_reheader', 'GRCh38.d1.vd1.dict')

    #cat new@SQ to orig header
    cmd = ['cat',gdc_sq_header_path, '>>', reheader]
    shell_cmd = ' '.join(cmd)
    output = subprocess.check_output(shell_cmd, shell=True)

    #add program info to new header
    cmd = ['tail', '-n', '+2', orig_bam_header_path, '>>', reheader]
    shell_cmd = ' '.join(cmd)
    output = subprocess.check_output(shell_cmd, shell=True)

    #reheader BAM
    samtools_path = os.path.join('/usr', 'local', 'bin', 'samtools')
    cmd = [samtools_path, 'reheader', reheader, bam_path, '>', bam_name ]
    shell_cmd = ' '.join(cmd)
    output = subprocess.check_output(shell_cmd, shell=True)
    return bam_name

def main():
    parser = argparse.ArgumentParser('reheader a BAM to include gdc @SQ info')

    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)

    # Tool flags
    parser.add_argument('-b', '--bam_path',
                        required = True
    )

    args = parser.parse_args()
    bam_path = args.bam_path

    bam_name = os.path.basename(bam_path)
    logger = setup_logging(args, bam_name)

    bam_name = reheader_bam(bam_path, logger)
    
    return


if __name__ == '__main__':
    main()
