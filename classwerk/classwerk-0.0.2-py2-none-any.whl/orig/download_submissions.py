#!/usr/bin/env python
import git
import os
from subprocess import check_output
from datetime import datetime
from git import Repo

import github3
import subprocess
from classwerk.utils import *

def add_subparser(subparser):
    parser = subparser.add_parser("download-submissions", help='returns result of Travis for repos')    
    parser.add_argument('-t', '--tag', help='name of tag', required=True)
    parser.add_argument('-o', '--output', help='output directory', required=True)
    parser.add_argument('-F', '--filter', nargs='*', dest='filter', help='filter by team name', default=None)
    parser.set_defaults(command=download_submissions)

def download_submissions(args, gh_handle, **kwargs):
    if not os.path.isdir(args.output):
        print Colors.error("Output directory must exist!")
        sys.exit(1)
    print "Saving submissions into %s" % os.path.abspath(args.output)

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
                file_location = os.path.join(args.output, name)

                repo = Repo.clone_from(repo_path, file_location)
                print "  \-> %s" % Colors.success("Saved submission to %s" % file_location)




