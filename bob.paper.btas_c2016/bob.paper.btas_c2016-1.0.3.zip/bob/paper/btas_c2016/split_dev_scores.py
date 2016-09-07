#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# E d MMM H:m:s z yyyy
#
# Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the ipyplotied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import argparse

import numpy
import os.path

import antispoofing.utils.db
import bob.io.base

# setup logging
import bob.core
logger = bob.core.log.setup("BTASLogger")


def find_in_scores(score_lines, cur_path):
    for line in score_lines:
        if cur_path in line:
            return float(line.split(' ')[1])
    return None

def write_scores(objs, out_file_name, score_lines):
    out_file = open(out_file_name, 'w')
    for obj in objs:
        cur_path = obj.make_path()
        id_str = (str(obj.get_client_id())).zfill(3)
        cur_score = find_in_scores(score_lines, cur_path)
        if cur_score is not None:
            logger.info("%s %f", cur_path, cur_score)
            out_file.write("%s %s %s %.10f\n" % (id_str, id_str, cur_path, cur_score))
        else:
            logger.error("Could not find score for %s", cur_path)
            raise
    out_file.close()

def main(command_line_parameters=None):

    basedir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
    parser.add_argument('-i', '--input-file', type=str, help='File with Dev scores')

    #######
    # Database specific configuration
    #######
    antispoofing.utils.db.Database.create_parser(parser, implements_any_of='audio')

    # add verbose option
    bob.core.log.add_command_line_option(parser)
    args = parser.parse_args()
    # set verbosity level
    bob.core.log.set_verbosity_level(logger, args.verbose)

    ########################
    #Querying the database
    ########################
    # get genuine (real) and spoofed (attacks) data
    database = args.cls(args)
    realObjects, attackObjects = database.get_devel_data()
    if realObjects == [] or attackObjects == []:
        logger.info('Development set is empty.')
    else:
        logger.info('Starting to process data from the Dev set')

        score_file = open(args.input_file, 'r')
        score_lines = score_file.readlines()
        score_file.close()

        submission_dir = os.path.dirname(args.input_file)
        out_file = os.path.join(submission_dir, 'dev-scores-real.txt')
        write_scores(realObjects, out_file, score_lines)
        out_file = os.path.join(submission_dir, 'dev-scores-attack.txt')
        write_scores(attackObjects, out_file, score_lines)

    logger.info("I'm done running!")


if __name__ == '__main__':
    main()