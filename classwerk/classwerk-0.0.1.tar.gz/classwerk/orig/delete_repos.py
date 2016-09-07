#!/usr/bin/env python
import os
import sys
from subprocess import Popen

import github3
from git import Repo
from travispy import TravisPy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from classwerk.utils import *


def add_subparser(subparser):
    parser = subparser.add_parser("delete-repos", help='delete repos and teams')
    parser.add_argument('--force',  action='store_const', const=True,  help='filter by team name', default=False)
    parser.add_argument('-F', '--filter', nargs='*', dest='filter', help='filter by team name', default=None)
    parser.set_defaults(command=delete_repo)

def delete_repo(args, gh_handle, **kwargs):

    c = get_config(args.config)
    org = gh_handle.organization(c['organization'])
    all_teams = org.teams()

    print "=" * 80
    print "Deleting repositories for %s from %s" % (c['organization'], c['source'])
    print "=" * 80


    teams = filter_teams(c['teams'], args.filter)
    repos = []

    if args.force:

        # Generate list of repos to remove
        for team in teams:
            members = c['teams'][team]
            repos.append("%s-%s" % (c['prefix'], team))

        # Remove repos
        for repo in org.repositories():
            if repo.name in repos:
                print "-> %s" % repo.name
                repo.delete()
                print "  \-> %s" % Colors.success("Deleted repo")

        for team in org.teams():
            if team.name in repos:
                print "-> %s" % team.name
                team.delete()
                print "  \-> %s" % Colors.success("Deleted team")

    else:
        print "This is extremely destructive! If you are sure you want to remove everything, re-run this with --force"