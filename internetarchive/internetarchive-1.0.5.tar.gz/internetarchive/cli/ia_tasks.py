# -*- coding: utf-8 -*-
#
# The internetarchive module is a Python/CLI interface to Archive.org.
#
# Copyright (C) 2012-2016 Internet Archive
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Retrieve information about your catalog tasks.

usage:
    ia tasks [options]...
    ia tasks <identifier> [options]...
    ia tasks --help

options:
    -h, --help
    -v, --verbose                 Ouptut detailed information for each task.
    -t, --task=<task_id>...       Return information about the given task.
    -G, --get-task-log=<task_id>  Return the given tasks task log.
    -g, --green-rows              Return information about tasks that have not run.
    -b, --blue-rows               Return information about running tasks.
    -r, --red-rows                Return information about tasks that have failed.
    -p, --parameter=<k:v>...      Return tasks matching the given parameter.
    -j, --json                    Change ouptut format to JSONL.

"""
from __future__ import absolute_import, print_function, unicode_literals
import sys
import json
import six

from docopt import docopt, printable_usage
from schema import Schema, Use, Or, And, SchemaError

from internetarchive.cli.argparser import get_args_dict


def main(argv, session):
    args = docopt(__doc__, argv=argv)
    s = Schema({
        six.text_type: Use(bool),
        '--task': list,
        '--get-task-log': list,
        '--parameter': Use(lambda x: get_args_dict(x, query_string=True)),
    })
    try:
        args = s.validate(args)
    except SchemaError as exc:
        print('{0}\n{1}'.format(str(exc), printable_usage(__doc__)), file=sys.stderr)
        sys.exit(1)

    row_types = {
        -1: 'done',
        0: 'green',
        1: 'blue',
        2: 'red',
        9: 'brown',
    }

    task_type = None
    if args['--green-rows']:
        task_type = 'green'
    elif args['--blue-rows']:
        task_type = 'blue'
    elif args['--red-rows']:
        task_type = 'red'

    try:
        try:
            if args['<identifier>']:
                tasks = session.get_tasks(identifier=args['<identifier>'],
                                          task_type=task_type,
                                          params=args['--parameter'])
            elif args['--get-task-log']:
                task = session.get_tasks(task_ids=args['--get-task-log'],
                                         params=args['--parameter'])
                if task:
                    log = task[0].task_log()
                    sys.exit(print(log))
                else:
                    print('error retrieving task-log '
                          'for {0}\n'.format(args['--get-task-log']), file=sys.stderr)
                    sys.exit(1)
            elif args['--task']:
                tasks = session.get_tasks(task_ids=args['--task'],
                                          params=args['--parameter'])
            else:
                tasks = session.get_tasks(task_type=task_type, params=args['--parameter'])
        except ValueError as exc:
            print('error: unable to parse JSON. have you run `ia configure`?'.format(exc),
                  file=sys.stderr)
            sys.exit(1)

        for t in tasks:
            if args['--json'] is True:
                print(json.dumps(t.task_dict))
            else:
                task_info = [t.identifier, t.task_id, t.server, t.time, t.command, t.row_type]
                if args['--verbose']:
                    # parse task args and append to task_info list.
                    targs = '\t'.join(
                        ['{0}={1}'.format(k, v) for (k, v) in t.args.items()])
                    task_info += [t.submitter, targs]
                print('\t'.join([str(x) for x in task_info]))
    except NameError as exc:
        print('error: {0}'.format(exc.message), file=sys.stderr)
        sys.exit(1)
