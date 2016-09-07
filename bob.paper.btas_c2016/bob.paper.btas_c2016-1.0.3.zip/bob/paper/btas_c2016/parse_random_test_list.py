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


def write_correct_lists(objs, file_real_name, file_attack_name, matching_dict_left2right, matching_dict_right2lef, anchor_real_lines, anchor_attack_lines):
    out_file_real = open(file_real_name, 'w')
    out_file_attack = open(file_attack_name, 'w')
    for obj in objs:
        cur_path = obj.make_path()
        correct_file_name = matching_dict_right2lef[cur_path.split('/')[1]]

        # if this file is an anchor file from Dev set, ignore it
        if (correct_file_name in anchor_real_lines) or (correct_file_name in anchor_attack_lines):
            continue

        logger.info("%s %s", cur_path, correct_file_name)
        # check if it's real or an attack
        if 'genuine' in correct_file_name:
            # extract id str from the file name (since in database, everything is hidden)
            id_str = correct_file_name.split('/')[2][1:]
            out_file_real.write("%s %s.wav genuine\n" % (id_str, cur_path))
        else:
            # extract id str from the file name (since in database, everything is hidden)
            id_str = correct_file_name.split('/')[3][1:]
            v = os.path.splitext(correct_file_name)[0].split('/')
            attackname = v[1]
            out_file_attack.write("%s %s.wav %s\n" % (id_str, cur_path, attackname))
    out_file_attack.close()
    out_file_real.close()

    # now, output anchore files too in two separate files
    out_file_real = open(os.path.splitext(file_real_name)[0] + '-anchors.txt', 'w')
    out_file_attack = open(os.path.splitext(file_attack_name)[0] + '-anchors.txt', 'w')
    anchor_lines = anchor_real_lines + anchor_attack_lines
    for line in anchor_lines:
        correct_file_name = line.strip()
        cur_path = matching_dict_left2right[correct_file_name]
        logger.info("%s %s", cur_path, correct_file_name)
        # check if it's real or an attack
        if 'genuine' in correct_file_name:
            # extract id str from the file name (since in database, everything is hidden)
            id_str = correct_file_name.split('/')[2][1:]
            out_file_real.write("%s %s.wav genuine\n" % (id_str, cur_path))
        else:
            # extract id str from the file name (since in database, everything is hidden)
            id_str = correct_file_name.split('/')[3][1:]
            v = os.path.splitext(correct_file_name)[0].split('/')
            attackname = v[1]
            out_file_attack.write("%s %s.wav %s\n" % (id_str, cur_path, attackname))

    out_file_attack.close()
    out_file_real.close()

def line2dict(lines, right2left=False):
    res_dict = {}
    for line in lines:
        sline = line.strip().split(' ')
        if right2left:
            key = sline[1].split('.wav')[0]
            value = sline[0]
        else:
            key = sline[0].split('.wav')[0]
            value = sline[1]
        if 'T' in key:
            key = key.split('/')[1]
        res_dict[key] = value
    return res_dict


def main(command_line_parameters=None):

    basedir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
    parser.add_argument('-r', '--real-anchor', type=str, help='Anchor file with real data from Dev set')
    parser.add_argument('-a', '--attack-anchor', type=str, help='Anchor file with attack data from Dev set')
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

        # parse matching names left2right
        matching_dict_left2right = line2dict(open(args.match_file, 'r').readlines())

        # read anchor files in lists
        with open(args.real_anchor) as f:
            anchor_real_lines = [line.rstrip() for line in f]
        with open(args.attack_anchor) as f:
            anchor_attack_lines = [line.rstrip() for line in f]

        matching_dict_right2left = line2dict(open(args.match_file, 'r').readlines(), right2left=True)
        submission_dir = os.path.dirname('.')
        out_file_real = os.path.join(submission_dir, 'test-real-list-derandomized.txt')
        out_file_attack = os.path.join(submission_dir, 'test-attack-list-derandomized.txt')
        write_correct_lists(realObjects, out_file_real, out_file_attack, matching_dict_left2right, matching_dict_right2left, anchor_real_lines, anchor_attack_lines)

    logger.info("I'm done running!")


if __name__ == '__main__':
    main()