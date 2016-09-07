#!/usr/bin/env python
import tempfile

import github3

from classwerk.utils import *

def add_subparser(subparser):
    parser = subparser.add_parser("create-teams", help='manage student groups')
    parser.add_argument('-F', '--filter', nargs='*', dest='filter', help='filter by team name', default=None)
    parser.set_defaults(command=create_teams)

def create_teams(args, gh_handle, **kwargs):

    c = get_config(args.config)
    org = gh_handle.organization(c['organization'])

    teams = filter_teams(c['teams'], args.filter)

    for team in teams:
        members = c['teams'][team]

        team_name = "%s-%s" % (c['prefix'], team)

        print "-> %s" % team

        # Create teams on Github
        try:
            team = org.create_team(team_name, permission='push')
            print "  \-> %s" % Colors.success("Created team")

        except github3.exceptions.UnprocessableEntity:
            print "  \-> %s" % Colors.warn("Team exists")
            # Team probably exists, so find it
            for avail_team in org.teams():
                if avail_team.name == team_name:
                    team = avail_team

        # Invite team members
        for member in members:
            team.invite(member)
            print "  \-> %s" % Colors.success("Invited %s" % member)

        # Remove members no longer in a group
        for prev_member in team.members():
            if prev_member.login not in members:
                team.remove_member(prev_member)
