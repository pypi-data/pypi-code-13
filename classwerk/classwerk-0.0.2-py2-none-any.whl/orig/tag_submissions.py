#!/usr/bin/env python
import git
from datetime import datetime
from git import Repo

import github3
from classwerk.utils import *

def add_subparser(subparser):
    parser = subparser.add_parser("tag-submissions", help='tag all student repos')
    parser.add_argument('-t', '--tag', help='name of tag', required=True)
    parser.add_argument('-m', '--message', help='message for tag', required=True)
    parser.set_defaults(command=add_tag)

def add_tag(args, gh_handle, **kwargs):
    c = get_config(args.config)
    org = gh_handle.organization(c['organization'])

    for team in c['teams']:
        members = c['teams'][team]

        name = "%s-%s" % (c['prefix'], team)
        repo_path = "git@github.com:%s/%s.git" % (c['organization'], name)
        repo_short = "%s/%s" % (c['organization'], name)

        print "-> %s" % name

        for repo in org.repositories():
            if repo.name == name:
                repo.create_release(args.tag, "master", name=args.tag, body=args.message)
                print "  \-> %s" % Colors.success("Created release")


