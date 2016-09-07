#!/usr/bin/env python
import git
import os
from subprocess import check_output
from datetime import datetime
from git import Repo

import github3
from classwerk.utils import *

def add_subparser(subparser):
    parser = subparser.add_parser("collect-results", help='returns result of Travis for repos')    
    parser.add_argument('-t', '--tag', help='name of tag', required=True)
    parser.add_argument('-o', '--output', help='output directory', required=True)
    parser.add_argument('-F', '--filter', nargs='*', dest='filter', help='filter by team name', default=None)
    parser.set_defaults(command=collect_results)

def collect_results(args, gh_handle, **kwargs):
    if not os.path.isdir(args.output):
        print Colors.error("Output directory must exist!")
        sys.exit(1)

    c = get_config(args.config)
    org = gh_handle.organization(c['organization'])
    all_repos = org.repositories()

    teams = filter_teams(c['teams'], args.filter)

    for team in teams:
        members = c['teams'][team]

        name = "%s-%s" % (c['prefix'], team)
        repo_path = "git@github.com:%s/%s.git" % (c['organization'], name)
        repo_short = "%s/%s" % (c['organization'], name)

        print "-> %s" % name
        FNULL = open(os.devnull, 'w')

        for repo in all_repos:
            if repo.name == name:
                # repo.create_release(args.tag, "master", name=args.tag, body=args.message)
                travis_build_number = check_output("travis branches -r %s | grep '^%s:' | awk -F' ' '{print $2}'" % (repo_short, args.tag), shell=True).strip()
                if travis_build_number == "":
                    print "  \-> %s" % Colors.error("Build not found")
                else:
                    travis_output = check_output("travis logs %s -r %s" % (travis_build_number[1:], repo_short), stderr=FNULL, shell=True)
                    print "  \-> %s" % Colors.success("Collected output")

                    # Write to file
                    output_file = os.path.join(args.output, '%s.txt' % name)
                    with open(output_file, 'w') as f:
                        f.write(travis_output)
                    print "  \-> %s" % Colors.success("Wrote to file [%s]" % output_file)




