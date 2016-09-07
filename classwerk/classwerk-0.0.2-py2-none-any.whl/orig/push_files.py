#!/usr/bin/env python
import git
from git import Repo

from classwerk.utils import *

def add_subparser(subparser):
    parser = subparser.add_parser("push-files", help='push code to student repos')
    parser.add_argument('-F', '--filter', nargs='*', dest='filter', help='filter by team name', default=None)
    parser.set_defaults(command=update_files)

def update_files(args, gh_handle, **kwargs):
    c = get_config(args.config)
    org = gh_handle.organization(c['organization'])

    teams = filter_teams(c['teams'], args.filter)

    teams_with_failure = []
    for team in teams:
        members = c['teams'][team]

        name = "%s-%s" % (c['prefix'], team)
        repo_path = "git@github.com:%s/%s.git" % (c['organization'], name)
        repo_short = "%s/%s" % (c['organization'], name)

        print "-> %s" % name

        # Check if github repo for team exists
        with TemporaryDirectory() as temp_dir:
            repo = Repo.clone_from(repo_path, temp_dir)
            print "  \-> Cloned student repo from %s" % repo_path

            upstream = repo.create_remote('upstream', c['source'])
            upstream.fetch()

            print "  \-> Fetched latest upstream"
            repo.git.checkout('upstream/%s' % c['source-branch'], track=True, b='upstream')
            repo.heads.upstream.checkout()

            repo.heads.master.checkout()
            try:
                repo.git.merge('upstream')
                print "  \-> %s" % Colors.success("Merged latest upstream")
            except git.exc.GitCommandError as e:
                repo.git.merge(abort=True)
                repo.git.checkout('upstream/%s' % c['source-branch'], track=True, b='merge-this')
                repo.remotes.origin.push('merge-this')
                teams_with_failure.append(name)

                print "  \-> %s" % Colors.error("Failed to merge latest upstream (conflicts). Pushed to merge-this branch")


            repo.remotes.origin.push(all=True)
            print "  \-> Pushed all branches"
    print "-> The following repositories had merge conflicts. Please notify these students and ask them to merge the 'merge-this' branch into master"
    for team in teams_with_failure:
        print "  -> %s" % team

