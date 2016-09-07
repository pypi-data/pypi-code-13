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


def write_split_scores(objs, file_real_name, file_attack_name, matching_dict, score_dict, anchor_real_lines, anchor_attack_lines):
    out_file_real = open(file_real_name, 'w')
    out_file_attack = open(file_attack_name, 'w')
    for obj in objs:
        cur_path = obj.make_path()
        correct_file_name = matching_dict[cur_path.split('/')[1]]
        
        # if this file is an anchor file from Dev set, ignore it
        if (correct_file_name in anchor_real_lines) or (correct_file_name in anchor_attack_lines):
            continue
        
        cur_score = float(score_dict[cur_path.split('/')[1]])
        logger.info("%s %f", cur_path, cur_score)
        # check if it's real or an attack
        if 'genuine' in correct_file_name:
            # extract id str from the file name (since in database, everything is hidden)
            id_str = correct_file_name.split('/')[2][1:]
            out_file_real.write("%s %s %s %.10f\n" % (id_str, id_str, correct_file_name, cur_score))
        else:
            # extract id str from the file name (since in database, everything is hidden)
            id_str = correct_file_name.split('/')[3][1:]
            out_file_attack.write("%s %s %s %.10f\n" % (id_str, id_str, correct_file_name, cur_score))

    out_file_attack.close()
    out_file_real.close()

def line2dict(lines, four_columns=False, right2left=False):
    res_dict = {}
    for line in lines:
        sline = line.strip().split(' ')
        if right2left:
            key = sline[1].split('.wav')[0]
            value = sline[0]
        else:
            key = sline[0].split('.wav')[0]
            value = sline[1]
        if four_columns:
            key = sline[2].split('.wav')[0]
            value = sline[3]
        if 'T' in key:
            key = key.split('/')[1]
        if 'T' in value:
            value = value.split('/')[1]
        res_dict[key] = value
    return res_dict


def check_anchor_scores(matching_dict, dev_score_dict, anchor_real_lines, anchor_attack_lines, score_dict):

    mismatch_counter = 0
    no_mismatch = True
    anchor_lines = anchor_real_lines + anchor_attack_lines
    # look among Dev real anchor names
    for line in anchor_lines:
        scrambled_test_file = matching_dict[line.strip()]
        test_score = None
        try:
            test_score = score_dict[scrambled_test_file]
        except Exception:
            logger.error("Could not find for anchor %s (scrambled: %s) score in Test set", line, scrambled_test_file)
            return False

        dev_score = dev_score_dict[line.strip()]
        if (float(dev_score) - float(test_score)) > 0.001:
            logger.error("For anchor file %s (randomized file: %s) Dev score %s and Test score %s do not match!",
                         line.strip(), scrambled_test_file, dev_score, test_score)
            no_mismatch = False
            mismatch_counter += 1
    logger.error("The number of anchor files = %d, the number of mismatched files = %d", len(anchor_lines), mismatch_counter)
    return no_mismatch

def main(command_line_parameters=None):

    basedir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
    parser.add_argument('-i', '--input-file', type=str, help='File with Test scores')
    parser.add_argument('-r', '--real-anchor', type=str, help='Anchor file with real data from Dev set')
    parser.add_argument('-a', '--attack-anchor', type=str, help='Anchor file with attack data from Dev set')
    parser.add_argument('-d', '--dev-scores', type=str, help='Scores from Dev set')
    parser.add_argument('-m', '--match-file', type=str, help='File with the randomized names matching to the real names')

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
    realObjects, attackObjects = database.get_test_data()
    # we process only RealObjects, because avspoof_btas2016 database contains
    # randomized files that are all labeled as 'real'
    if realObjects == []:
        logger.info('Test set is empty.')
    else:
        logger.info('Starting to process data from the Dev set')

        # parse matching names
        matching_dict = line2dict(open(args.match_file, 'r').readlines())

        score_dict = line2dict(open(args.input_file, 'r').readlines())
        dev_score_dict = line2dict(open(args.dev_scores, 'r').readlines())
        # dev_score_dict = line2dict(open(args.dev_scores, 'r').readlines(), four_columns=True)
        
        # read anchor files in lists
        with open(args.real_anchor) as f:
            anchor_real_lines = [line.rstrip() for line in f]
        with open(args.attack_anchor) as f:
            anchor_attack_lines = [line.rstrip() for line in f]

        # check scores for anchor files from the Dev set
        all_correct = check_anchor_scores(matching_dict, dev_score_dict, anchor_real_lines, anchor_attack_lines, score_dict)
        if all_correct:
            logger.error("All anchor scores matched correctly!")
        else:
            logger.info("Anchor scores do not match!!")

        matching_dict = line2dict(open(args.match_file, 'r').readlines(), right2left=True)
        submission_dir = os.path.dirname(args.input_file)
        out_file_real = os.path.join(submission_dir, 'test-scores-real.txt')
        out_file_attack = os.path.join(submission_dir, 'test-scores-attack.txt')
        write_split_scores(realObjects, out_file_real, out_file_attack, matching_dict, score_dict, anchor_real_lines, anchor_attack_lines)

    logger.info("I'm done running!")


if __name__ == '__main__':
    main()